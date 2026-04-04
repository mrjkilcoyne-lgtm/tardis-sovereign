import SwiftUI

// MARK: - Quick Select Pill

struct QuickSelectPill: Identifiable {
    let id = UUID()
    let label: String
    let icon: String
    let situation: String
}

private let quickPills: [QuickSelectPill] = [
    QuickSelectPill(label: "Press", icon: "newspaper", situation: "press conference media coverage"),
    QuickSelectPill(label: "Concert", icon: "music.note", situation: "concert live music event"),
    QuickSelectPill(label: "Flight", icon: "airplane", situation: "airport flight boarding gate"),
    QuickSelectPill(label: "Security", icon: "lock.shield", situation: "security restricted classified facility"),
    QuickSelectPill(label: "Conference", icon: "person.badge.key", situation: "tech conference summit developer"),
    QuickSelectPill(label: "Travel", icon: "tram", situation: "metro train bus transport commute"),
]

// MARK: - Content View

struct ContentView: View {
    @State private var identity = Identity.load()
    @State private var situationText = ""
    @State private var currentDocument: GeneratedDocument?
    @State private var documentType: DocumentType = .press_pass
    @State private var isMorphing = false
    @State private var rotationAngle: Double = 0
    @State private var showSettings = false

    var body: some View {
        ZStack {
            // Background
            Color(red: 0.04, green: 0.04, blue: 0.04)
                .ignoresSafeArea()

            // Subtle ambient glow behind document
            if let doc = currentDocument {
                doc.documentType.colors.primary.opacity(0.08)
                    .blur(radius: 100)
                    .ignoresSafeArea()
                    .animation(.easeInOut(duration: 1.0), value: doc.documentType)
            }

            VStack(spacing: 0) {
                // Top bar
                headerBar

                ScrollView(.vertical, showsIndicators: false) {
                    VStack(spacing: 24) {
                        // Situation input
                        situationInput

                        // The morphing paper
                        paperDisplay
                            .padding(.top, 8)

                        // Quick select pills
                        quickSelectRow

                        Spacer(minLength: 40)
                    }
                    .padding(.top, 8)
                }
            }
        }
        .onAppear {
            morphTo(situation: "press conference")
        }
        .sheet(isPresented: $showSettings) {
            settingsSheet
        }
    }

    // MARK: - Header

    private var headerBar: some View {
        HStack {
            VStack(alignment: .leading, spacing: 2) {
                Text("PSYCHIC PAPER")
                    .font(.system(size: 11, weight: .bold))
                    .tracking(3)
                    .foregroundColor(.white.opacity(0.4))
                Text(identity.name)
                    .font(.system(size: 15, weight: .medium))
                    .foregroundColor(.white.opacity(0.7))
            }

            Spacer()

            Button {
                showSettings = true
            } label: {
                Image(systemName: "person.crop.circle")
                    .font(.system(size: 20))
                    .foregroundColor(.white.opacity(0.4))
            }
        }
        .padding(.horizontal, 20)
        .padding(.vertical, 12)
    }

    // MARK: - Situation Input

    private var situationInput: some View {
        HStack(spacing: 12) {
            Image(systemName: "sparkle")
                .font(.system(size: 14))
                .foregroundColor(.white.opacity(0.3))

            TextField(
                "",
                text: $situationText,
                prompt: Text("Describe the situation...")
                    .foregroundColor(.white.opacity(0.2))
            )
            .font(.system(size: 15, weight: .regular))
            .foregroundColor(.white)
            .textInputAutocapitalization(.never)
            .autocorrectionDisabled()
            .onSubmit {
                if !situationText.isEmpty {
                    morphTo(situation: situationText)
                }
            }

            if !situationText.isEmpty {
                Button {
                    morphTo(situation: situationText)
                } label: {
                    Image(systemName: "arrow.right.circle.fill")
                        .font(.system(size: 22))
                        .foregroundColor(.white.opacity(0.6))
                }
            }
        }
        .padding(.horizontal, 16)
        .padding(.vertical, 14)
        .background(
            RoundedRectangle(cornerRadius: 14)
                .fill(Color.white.opacity(0.05))
                .overlay(
                    RoundedRectangle(cornerRadius: 14)
                        .strokeBorder(Color.white.opacity(0.06), lineWidth: 1)
                )
        )
        .padding(.horizontal, 20)
    }

    // MARK: - Paper Display

    private var paperDisplay: some View {
        Group {
            if let doc = currentDocument {
                PaperView(document: doc)
                    .rotation3DEffect(
                        .degrees(rotationAngle),
                        axis: (x: 0, y: 1, z: 0),
                        perspective: 0.4
                    )
                    .opacity(isMorphing ? 0 : 1)
                    .scaleEffect(isMorphing ? 0.9 : 1.0)

                // Document type label
                HStack(spacing: 6) {
                    Circle()
                        .fill(doc.documentType.colors.accent)
                        .frame(width: 6, height: 6)
                    Text(doc.documentType.displayName)
                        .font(.system(size: 12, weight: .medium))
                        .foregroundColor(.white.opacity(0.4))
                        .tracking(1)
                }
                .padding(.top, 12)
                .transition(.opacity)
                .animation(.easeInOut(duration: 0.3), value: doc.documentType)
            } else {
                // Placeholder
                RoundedRectangle(cornerRadius: 16)
                    .fill(Color.white.opacity(0.03))
                    .frame(height: 220)
                    .padding(.horizontal, 24)
                    .overlay(
                        VStack(spacing: 8) {
                            Image(systemName: "doc.viewfinder")
                                .font(.system(size: 32, weight: .thin))
                            Text("Describe a situation")
                                .font(.system(size: 13, weight: .light))
                        }
                        .foregroundColor(.white.opacity(0.15))
                    )
            }
        }
    }

    // MARK: - Quick Select

    private var quickSelectRow: some View {
        ScrollView(.horizontal, showsIndicators: false) {
            HStack(spacing: 10) {
                ForEach(quickPills) { pill in
                    Button {
                        situationText = pill.situation
                        morphTo(situation: pill.situation)
                    } label: {
                        HStack(spacing: 6) {
                            Image(systemName: pill.icon)
                                .font(.system(size: 11))
                            Text(pill.label)
                                .font(.system(size: 12, weight: .medium))
                        }
                        .foregroundColor(
                            isPillActive(pill) ? .black : .white.opacity(0.5)
                        )
                        .padding(.horizontal, 14)
                        .padding(.vertical, 8)
                        .background(
                            Capsule().fill(
                                isPillActive(pill)
                                    ? Color.white
                                    : Color.white.opacity(0.06)
                            )
                        )
                    }
                }
            }
            .padding(.horizontal, 20)
        }
    }

    private func isPillActive(_ pill: QuickSelectPill) -> Bool {
        guard let doc = currentDocument else { return false }
        let detected = ContextDetector.detect(situation: pill.situation)
        return doc.documentType == detected
    }

    // MARK: - Settings Sheet

    private var settingsSheet: some View {
        NavigationStack {
            ZStack {
                Color(red: 0.06, green: 0.06, blue: 0.06).ignoresSafeArea()

                VStack(spacing: 24) {
                    settingsField(label: "NAME", value: $identity.name)
                    settingsField(label: "ORGANISATION", value: $identity.organisation)
                    settingsField(label: "TITLE", value: $identity.title)

                    Spacer()

                    Button {
                        identity.save()
                        // Regenerate current document with new identity
                        if let doc = currentDocument {
                            currentDocument = DocumentGenerator.generate(
                                identity: identity, documentType: doc.documentType
                            )
                        }
                        showSettings = false
                    } label: {
                        Text("Save")
                            .font(.system(size: 16, weight: .medium))
                            .tracking(1)
                            .foregroundColor(.black)
                            .frame(maxWidth: .infinity)
                            .frame(height: 50)
                            .background(Color.white)
                            .clipShape(Capsule())
                    }
                    .padding(.bottom, 20)
                }
                .padding(24)
            }
            .navigationTitle("Identity")
            .navigationBarTitleDisplayMode(.inline)
            .toolbar {
                ToolbarItem(placement: .topBarLeading) {
                    Button("Cancel") { showSettings = false }
                        .foregroundColor(.white.opacity(0.5))
                }
            }
        }
        .presentationDetents([.medium])
        .preferredColorScheme(.dark)
    }

    private func settingsField(label: String, value: Binding<String>) -> some View {
        VStack(alignment: .leading, spacing: 6) {
            Text(label)
                .font(.system(size: 10, weight: .bold))
                .tracking(2)
                .foregroundColor(.white.opacity(0.4))
            TextField("", text: value)
                .font(.system(size: 17, weight: .regular))
                .foregroundColor(.white)
                .padding(.vertical, 12)
                .padding(.horizontal, 14)
                .background(
                    RoundedRectangle(cornerRadius: 10)
                        .fill(Color.white.opacity(0.05))
                )
        }
    }

    // MARK: - Morph Logic

    private func morphTo(situation: String) {
        let newType = ContextDetector.detect(situation: situation)

        guard newType != currentDocument?.documentType || currentDocument == nil else { return }

        // Phase 1: flip out
        withAnimation(.easeIn(duration: 0.25)) {
            isMorphing = true
            rotationAngle = 90
        }

        // Phase 2: swap content + flip in
        DispatchQueue.main.asyncAfter(deadline: .now() + 0.25) {
            let doc = DocumentGenerator.generate(identity: identity, documentType: newType)
            currentDocument = doc
            rotationAngle = -90

            withAnimation(.spring(response: 0.5, dampingFraction: 0.75)) {
                rotationAngle = 0
                isMorphing = false
            }
        }
    }
}

#Preview {
    ContentView()
        .preferredColorScheme(.dark)
}
