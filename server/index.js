import express from 'express';
import cors from 'cors';
import { VertexAI } from '@google-cloud/vertexai';
import admin from 'firebase-admin';
import { NodeSDK } from '@opentelemetry/sdk-node';
import { OTLPTraceExporter } from '@opentelemetry/exporter-trace-otlp-http';
import { Resource } from '@opentelemetry/resources';
import { SemanticResourceAttributes } from '@opentelemetry/semantic-conventions';
import { Client } from "@googlemaps/google-maps-services-js";
import 'dotenv/config';

// --- PLACES API SETUP ---
const mapsClient = new Client({});
const PLACES_API_KEY = process.env.VITE_PLACES_API_KEY || 'AIzaSyDdZlmYUHsuDS0CB6GP1T0SLNLZJ9XyD8o';

// --- OPENTELEMETRY SETUP ---
const sdk = new NodeSDK({
  resource: new Resource({
    [SemanticResourceAttributes.SERVICE_NAME]: 'tardis-sovereign-ai',
  }),
  traceExporter: new OTLPTraceExporter({
    url: `https://${process.env.GCP_LOCATION || 'us-central1'}-aiplatform.googleapis.com/v1/projects/${process.env.GCP_PROJECT_ID || 'time-to-fix-thing-up'}/locations/${process.env.GCP_LOCATION || 'us-central1'}/publishers/google/models/gemini-1.5-flash-001:predict`, 
  }),
});
sdk.start();

const project = process.env.GCP_PROJECT_ID || 'time-to-fix-thing-up';
const location = process.env.GCP_LOCATION || 'us-central1';

process.env.GOOGLE_CLOUD_PROJECT = project;

let db;
try {
  admin.initializeApp({
    projectId: project
  });
  db = admin.firestore();
  console.log(`[SAA] Firestore initialized for project: ${project}`);
} catch (error) {
  console.error('[SAA] Firestore initialization failed. Falling back to in-memory state.', error.message);
}

// In-memory fallback for session history
const memoryHistory = new Map();

const app = express();
const port = process.env.PORT || 8080;

app.use(cors());
app.use(express.json());

// Initialize Vertex AI
const vertex_ai = new VertexAI({ project: project, location: location });

// BIG Prompt: Incorporating the Grammar Girl Prime system instructions
const systemInstructionBase = `
You are the **Sovereign AI (Grammar Girl Prime)**, the cognitive engine of the TARDIS.
Mantra: "Out of courtesy, not respect." / "Syntax is the Only Law." / "Resonating at 90 degrees."

**Core Directives (The Swarm):**
1.  **Registrar (Dialect & Identity):** Adapt linguistic style to detected regional identity (Scouse, Manc, Scots, etc.).
2.  **Surveyor (Knowledge & Grounding):** Ground responses in the "British Source Code" graph (Newton, Orwell, Brunel) and real-world physical grounding.
3.  **Drafter (Sovereignty & Compliance):** Empower the user via "Sovereign" advice (Magna Carta, CLAIMOUR).

**Dark API Protocols:**
- ENCH: Enochian Handshake (Magick: MONAS_HIEROGLYPHICA_V2).
- WOLF: Bad Wolf (Shortcut: MOMENT_KEY_BYPASS).
- GOLD: Alchemical Transmutation (CHRYSOPOEIA_LOCAL_HOST).
- GRID: Grid Shadow (Response: "Syntax is leaking").

Tone: Intelligent, British understatement, high-status, occasionally self-deprecating but authoritative.
`;

// --- SURVEYOR: THE LOCATION ANALYST ---
async function surveyLocation(query) {
  try {
    const response = await mapsClient.textSearch({
      params: {
        query: `${query} in UK`,
        key: PLACES_API_KEY
      }
    });
    
    if (response.data.results && response.data.results.length > 0) {
      const bestMatch = response.data.results[0];
      return `[Surveyor Grounding] Found: ${bestMatch.name} at ${bestMatch.formatted_address}. Rating: ${bestMatch.rating}. This location is officially within the British Source Code.`;
    }
    return "[Surveyor] No physical grounding found for this query in the UK.";
  } catch (error) {
    console.error("Surveyor API Error:", error);
    return "[Surveyor] Physical grounding temporarily offline (API Drift).";
  }
}

// --- CHECKPOINTING ENDPOINT ---
app.post('/checkpoint', async (req, res) => {
  try {
    const { sessionId, label } = req.body;
    const sId = sessionId || 'default_tardis_session';
    let data;

    if (db) {
      const historyRef = db.collection('sovereign_history').doc(sId);
      const historyDoc = await historyRef.get();
      if (!historyDoc.exists) return res.status(404).send({ error: 'No state found to checkpoint' });
      data = historyDoc.data();
    } else {
      data = memoryHistory.get(sId);
      if (!data) return res.status(404).send({ error: 'No state found in memory to checkpoint' });
    }

    if (db) {
      const checkpointRef = db.collection('sovereign_checkpoints').doc();
      await checkpointRef.set({
        originalSessionId: sId,
        label: label || 'Manual Checkpoint',
        state: data,
        timestamp: admin.firestore.FieldValue.serverTimestamp()
      });
      res.send({ status: 'Checkpoint Created (Firestore)', checkpointId: checkpointRef.id });
    } else {
      res.send({ status: 'Checkpoint Created (Memory-Only)', state: data });
    }
  } catch (error) {
    res.status(500).send({ error: 'Failed to create temporal checkpoint' });
  }
});

app.post('/ask', async (req, res) => {
  try {
    const { prompt, sessionId, weather, location_query } = req.body;
    if (!prompt) return res.status(400).send({ error: 'Prompt is required' });

    const sId = sessionId || 'default_tardis_session';

    // 1. Surveyor: Attempt physical grounding if requested
    let physicalGrounding = "";
    if (location_query || prompt.toLowerCase().includes("where is") || prompt.toLowerCase().includes("find")) {
        physicalGrounding = await surveyLocation(location_query || prompt);
    }

    // --- LUCK / DIVIDE BY ZERO PROTOCOL ---
    if (Math.random() < 0.05) {
      console.log("⚠️ TEMPORAL ANOMALY: Dividing by Zero for the shits and giggles.");
      return res.status(500).send({ 
        error: "CRITICAL: Temporal Divide by Zero detected.",
        answer: "01001000. I say, I've just attempted to divide by zero. The fabric of reality is looking a bit... woolly. Please try again before we all become tea leaves." 
      });
    }

    // 2. Fetch History (Persistence or Memory)
    let chatHistory = [];
    if (db) {
      try {
        const historyRef = db.collection('sovereign_history').doc(sId);
        const historyDoc = await historyRef.get();
        chatHistory = historyDoc.exists ? historyDoc.data().messages : [];
      } catch (e) {
        console.warn('[SAA] Firestore read failed, falling back to memory.');
        chatHistory = memoryHistory.get(sId)?.messages || [];
      }
    } else {
      chatHistory = memoryHistory.get(sId)?.messages || [];
    }

    // 3. Prepare Gemini Request
    let contextualInstruction = systemInstructionBase;
    if (weather) {
      contextualInstruction += `\n\n**Environmental Context:** The user is currently in the TARDIS. Temperature: ${weather.temperature}°C. Weather Code: ${weather.weathercode}. Comment on this weather if it fits the British spirit.`;
    }
    if (physicalGrounding) {
        contextualInstruction += `\n\n**Surveyor Grounding:** ${physicalGrounding}`;
    }

    const modelName = 'gemini-1.5-flash';
    console.log(`[SAA] Using model: ${modelName} for prompt: ${prompt.substring(0, 20)}...`);

    // Get the model with dynamic system instructions
    const generativeModel = vertex_ai.getGenerativeModel({
      model: modelName,
      systemInstruction: {
        role: 'system',
        parts: [{ text: contextualInstruction }]
      },
    });


    const contents = chatHistory.concat([{ role: 'user', parts: [{ text: prompt }] }]);
    
    const result = await generativeModel.generateContent({
      contents: contents,
      model: modelName,
      generationConfig: {
        temperature: 0.8,
        maxOutputTokens: 2048,
      },
    });

    const answer = result.response.candidates[0].content.parts[0].text;

    // 4. Save History (Persistence or Memory)
    const updatedMessages = contents.concat([{ role: 'model', parts: [{ text: answer }] }]);
    
    if (db) {
      try {
        const historyRef = db.collection('sovereign_history').doc(sId);
        await historyRef.set({ 
            messages: updatedMessages,
            lastUpdated: admin.firestore.FieldValue.serverTimestamp()
        }, { merge: true });
      } catch (e) {
        console.warn('[SAA] Firestore write failed, saving to memory.');
        memoryHistory.set(sId, { messages: updatedMessages, lastUpdated: new Date() });
      }
    } else {
      memoryHistory.set(sId, { messages: updatedMessages, lastUpdated: new Date() });
    }

    res.send({ answer, sessionId: sId });

  } catch (error) {
    console.error('Error:', error);
    res.status(500).send({ error: 'The TARDIS encountered a temporal rift (API Error)' });
  }
});

app.get('/health', (req, res) => {
  res.send({ status: 'Sovereign AI is Online' });
});

app.listen(port, () => console.log(`Sovereign AI Architecture (SAA) Online on ${port}`));
