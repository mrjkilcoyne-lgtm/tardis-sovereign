import SwiftUI
import CoreImage.CIFilterBuiltins

// MARK: - Main Paper View

struct PaperView: View {
    let document: GeneratedDocument
    @State private var appear = false
    @State private var shimmerPhase: CGFloat = -1

    var body: some View {
        Group {
            switch document.documentType.layout {
            case .card:
                cardLayout
            case .ticket:
                ticketLayout
            case .badge:
                badgeLayout
            case .full:
                fullLayout
            }
        }
        .onAppear {
            withAnimation(.easeOut(duration: 0.6)) { appear = true }
            startShimmer()
        }
        .onChange(of: document.documentType) { _ in
            shimmerPhase = -1
            startShimmer()
        }
    }

    private func startShimmer() {
        withAnimation(.linear(duration: 2.5).repeatForever(autoreverses: false)) {
            shimmerPhase = 2
        }
    }

    // MARK: - Card Layout (credit-card ratio with hologram shimmer)

    private var cardLayout: some View {
        let colors = document.documentType.colors
        return ZStack {
            RoundedRectangle(cornerRadius: 16)
                .fill(
                    LinearGradient(
                        colors: [colors.background, colors.primary.opacity(0.4)],
                        startPoint: .topLeading,
                        endPoint: .bottomTrailing
                    )
                )

            // Hologram shimmer
            RoundedRectangle(cornerRadius: 16)
                .fill(
                    LinearGradient(
                        colors: [
                            .clear,
                            colors.accent.opacity(0.15),
                            colors.accent.opacity(0.3),
                            colors.accent.opacity(0.15),
                            .clear
                        ],
                        startPoint: UnitPoint(x: shimmerPhase - 0.3, y: 0),
                        endPoint: UnitPoint(x: shimmerPhase + 0.3, y: 1)
                    )
                )

            RoundedRectangle(cornerRadius: 16)
                .strokeBorder(colors.primary.opacity(0.4), lineWidth: 1)

            VStack(alignment: .leading, spacing: 0) {
                // Header
                HStack {
                    Image(systemName: document.documentType.icon)
                        .font(.system(size: 18, weight: .medium))
                        .foregroundColor(colors.accent)
                    Spacer()
                    Text(document.documentType.issuer)
                        .font(.system(size: 8, weight: .bold))
                        .tracking(2)
                        .foregroundColor(colors.textSecondary)
                }
                .padding(.bottom, 16)

                // Primary field (large)
                if let primary = document.fields.first {
                    Text(primary.value)
                        .font(.system(size: 20, weight: .semibold, design: .default))
                        .foregroundColor(colors.textPrimary)
                        .lineLimit(1)
                        .minimumScaleFactor(0.7)
                }

                Spacer()

                // Secondary fields in grid
                let secondaryFields = Array(document.fields.dropFirst().prefix(4))
                LazyVGrid(columns: [
                    GridItem(.flexible(), alignment: .leading),
                    GridItem(.flexible(), alignment: .leading)
                ], spacing: 8) {
                    ForEach(secondaryFields) { field in
                        VStack(alignment: .leading, spacing: 2) {
                            Text(field.label)
                                .font(.system(size: 7, weight: .bold))
                                .tracking(1)
                                .foregroundColor(colors.textSecondary)
                            Text(field.value)
                                .font(.system(size: 12, weight: .medium))
                                .foregroundColor(colors.textPrimary)
                                .lineLimit(1)
                        }
                    }
                }

                HStack {
                    Spacer()
                    qrCodeView(payload: document.qrPayload, size: 40, color: colors.accent)
                }
                .padding(.top, 8)
            }
            .padding(20)
        }
        .frame(height: 220)
        .padding(.horizontal, 24)
    }

    // MARK: - Ticket Layout (perforated edge + stub)

    private var ticketLayout: some View {
        let colors = document.documentType.colors
        return HStack(spacing: 0) {
            // Main ticket area
            ZStack {
                UnevenRoundedRectangle(
                    topLeadingRadius: 16,
                    bottomLeadingRadius: 16,
                    bottomTrailingRadius: 0,
                    topTrailingRadius: 0
                )
                .fill(
                    LinearGradient(
                        colors: [colors.background, colors.primary.opacity(0.3)],
                        startPoint: .topLeading,
                        endPoint: .bottomTrailing
                    )
                )

                UnevenRoundedRectangle(
                    topLeadingRadius: 16,
                    bottomLeadingRadius: 16,
                    bottomTrailingRadius: 0,
                    topTrailingRadius: 0
                )
                .strokeBorder(colors.primary.opacity(0.3), lineWidth: 1)

                VStack(alignment: .leading, spacing: 10) {
                    // Issuer
                    HStack {
                        Image(systemName: document.documentType.icon)
                            .foregroundColor(colors.accent)
                        Text(document.documentType.issuer)
                            .font(.system(size: 9, weight: .bold))
                            .tracking(2)
                            .foregroundColor(colors.accent)
                    }

                    // Event / primary
                    if let eventField = document.fields.first(where: { $0.label == "EVENT" }) {
                        Text(eventField.value)
                            .font(.system(size: 18, weight: .bold))
                            .foregroundColor(colors.textPrimary)
                            .lineLimit(2)
                    }

                    // Detail fields
                    let detailFields = document.fields.filter {
                        !["EVENT"].contains($0.label)
                    }.prefix(5)

                    ForEach(Array(detailFields)) { field in
                        HStack(spacing: 4) {
                            Text(field.label)
                                .font(.system(size: 8, weight: .bold))
                                .tracking(1)
                                .foregroundColor(colors.textSecondary)
                            Text(field.value)
                                .font(.system(size: 12, weight: .medium))
                                .foregroundColor(colors.textPrimary)
                                .lineLimit(1)
                        }
                    }

                    Spacer(minLength: 0)
                }
                .padding(16)
            }

            // Perforation
            VStack(spacing: 6) {
                ForEach(0..<16, id: \.self) { _ in
                    Circle()
                        .fill(Color(red: 0.04, green: 0.04, blue: 0.04))
                        .frame(width: 4, height: 4)
                }
            }
            .frame(width: 8)
            .background(colors.background.opacity(0.5))

            // Stub
            ZStack {
                UnevenRoundedRectangle(
                    topLeadingRadius: 0,
                    bottomLeadingRadius: 0,
                    bottomTrailingRadius: 16,
                    topTrailingRadius: 16
                )
                .fill(colors.background)

                UnevenRoundedRectangle(
                    topLeadingRadius: 0,
                    bottomLeadingRadius: 0,
                    bottomTrailingRadius: 16,
                    topTrailingRadius: 16
                )
                .strokeBorder(colors.primary.opacity(0.3), lineWidth: 1)

                VStack(spacing: 12) {
                    qrCodeView(payload: document.qrPayload, size: 56, color: colors.accent)

                    if let refField = document.fields.first(where: {
                        ["REF", "SEAT", "GATE"].contains($0.label)
                    }) {
                        VStack(spacing: 2) {
                            Text(refField.label)
                                .font(.system(size: 7, weight: .bold))
                                .tracking(1)
                                .foregroundColor(colors.textSecondary)
                            Text(refField.value)
                                .font(.system(size: 14, weight: .bold, design: .monospaced))
                                .foregroundColor(colors.accent)
                        }
                    }
                }
                .padding(12)
            }
            .frame(width: 90)
        }
        .frame(height: 240)
        .padding(.horizontal, 16)
    }

    // MARK: - Badge Layout (lanyard visual)

    private var badgeLayout: some View {
        let colors = document.documentType.colors
        return VStack(spacing: 0) {
            // Lanyard
            LanyardShape()
                .stroke(
                    LinearGradient(
                        colors: [colors.primary.opacity(0.6), colors.primary],
                        startPoint: .top,
                        endPoint: .bottom
                    ),
                    lineWidth: 3
                )
                .frame(height: 50)
                .padding(.horizontal, 80)

            // Badge clip
            RoundedRectangle(cornerRadius: 3)
                .fill(Color.gray.opacity(0.6))
                .frame(width: 40, height: 8)

            // Badge body
            ZStack {
                RoundedRectangle(cornerRadius: 16)
                    .fill(
                        LinearGradient(
                            colors: [colors.background, colors.primary.opacity(0.2)],
                            startPoint: .top,
                            endPoint: .bottom
                        )
                    )

                RoundedRectangle(cornerRadius: 16)
                    .strokeBorder(colors.primary.opacity(0.4), lineWidth: 1)

                VStack(spacing: 14) {
                    // Header bar
                    HStack {
                        Text(document.documentType.issuer)
                            .font(.system(size: 9, weight: .bold))
                            .tracking(2)
                            .foregroundColor(colors.accent)
                        Spacer()
                        Image(systemName: document.documentType.icon)
                            .foregroundColor(colors.accent)
                    }

                    // Avatar placeholder
                    Circle()
                        .fill(colors.primary.opacity(0.3))
                        .frame(width: 60, height: 60)
                        .overlay(
                            Text(initials(from: document.fields.first?.value ?? ""))
                                .font(.system(size: 22, weight: .bold))
                                .foregroundColor(colors.accent)
                        )

                    // Name
                    if let nameField = document.fields.first {
                        Text(nameField.value)
                            .font(.system(size: 22, weight: .bold))
                            .foregroundColor(colors.textPrimary)
                            .lineLimit(1)
                            .minimumScaleFactor(0.6)
                    }

                    // Title/role
                    if let titleField = document.fields.first(where: {
                        ["TITLE", "ACCESS LEVEL", "CLEARANCE"].contains($0.label)
                    }) {
                        Text(titleField.value)
                            .font(.system(size: 13, weight: .medium))
                            .foregroundColor(colors.textSecondary)
                    }

                    Divider().background(colors.primary.opacity(0.3))

                    // Detail fields
                    let detailFields = document.fields.filter {
                        !["NAME", "TITLE", "ACCESS LEVEL", "CLEARANCE"].contains($0.label)
                    }.prefix(3)

                    HStack(spacing: 16) {
                        ForEach(Array(detailFields)) { field in
                            VStack(spacing: 2) {
                                Text(field.label)
                                    .font(.system(size: 7, weight: .bold))
                                    .tracking(1)
                                    .foregroundColor(colors.textSecondary)
                                Text(field.value)
                                    .font(.system(size: 11, weight: .medium))
                                    .foregroundColor(colors.textPrimary)
                                    .lineLimit(1)
                            }
                        }
                    }

                    qrCodeView(payload: document.qrPayload, size: 48, color: colors.accent)
                }
                .padding(20)
            }
            .frame(height: 340)
            .padding(.horizontal, 32)
        }
    }

    // MARK: - Full Layout (permit / invitation - formal document)

    private var fullLayout: some View {
        let colors = document.documentType.colors
        return ZStack {
            RoundedRectangle(cornerRadius: 12)
                .fill(colors.background)

            RoundedRectangle(cornerRadius: 12)
                .strokeBorder(colors.primary.opacity(0.3), lineWidth: 1)

            // Inner border
            RoundedRectangle(cornerRadius: 8)
                .strokeBorder(colors.primary.opacity(0.15), lineWidth: 0.5)
                .padding(8)

            VStack(spacing: 16) {
                // Seal / header
                Image(systemName: document.documentType.icon)
                    .font(.system(size: 28, weight: .light))
                    .foregroundColor(colors.accent)

                Text(document.documentType.issuer)
                    .font(.system(size: 11, weight: .bold))
                    .tracking(4)
                    .foregroundColor(colors.accent)

                Rectangle()
                    .fill(colors.primary.opacity(0.2))
                    .frame(width: 60, height: 1)

                // All fields
                VStack(spacing: 10) {
                    ForEach(document.fields) { field in
                        VStack(spacing: 3) {
                            Text(field.label)
                                .font(.system(size: 8, weight: .bold))
                                .tracking(2)
                                .foregroundColor(colors.textSecondary)
                            Text(field.value)
                                .font(.system(size: 14, weight: .medium))
                                .foregroundColor(colors.textPrimary)
                                .multilineTextAlignment(.center)
                                .lineLimit(1)
                        }
                    }
                }

                Spacer(minLength: 0)

                HStack {
                    qrCodeView(payload: document.qrPayload, size: 44, color: colors.accent)
                    Spacer()
                    VStack(alignment: .trailing, spacing: 2) {
                        Text(document.documentType.displayName.uppercased())
                            .font(.system(size: 7, weight: .bold))
                            .tracking(2)
                            .foregroundColor(colors.textSecondary)
                        Text("VERIFIED")
                            .font(.system(size: 7, weight: .bold))
                            .tracking(2)
                            .foregroundColor(colors.accent)
                    }
                }
            }
            .padding(24)
        }
        .frame(height: 420)
        .padding(.horizontal, 24)
    }

    // MARK: - QR Code

    private func qrCodeView(payload: String, size: CGFloat, color: Color) -> some View {
        Group {
            if let image = generateQRCode(from: payload) {
                Image(uiImage: image)
                    .interpolation(.none)
                    .resizable()
                    .scaledToFit()
                    .frame(width: size, height: size)
                    .colorMultiply(color)
            } else {
                RoundedRectangle(cornerRadius: 4)
                    .fill(color.opacity(0.2))
                    .frame(width: size, height: size)
                    .overlay(
                        Image(systemName: "qrcode")
                            .foregroundColor(color)
                    )
            }
        }
    }

    private func generateQRCode(from string: String) -> UIImage? {
        let context = CIContext()
        let filter = CIFilter.qrCodeGenerator()
        filter.message = Data(string.utf8)
        filter.correctionLevel = "M"

        guard let output = filter.outputImage else { return nil }

        let scale = CGAffineTransform(scaleX: 10, y: 10)
        let scaled = output.transformed(by: scale)

        guard let cgImage = context.createCGImage(scaled, from: scaled.extent) else { return nil }
        return UIImage(cgImage: cgImage)
    }

    // MARK: - Helpers

    private func initials(from name: String) -> String {
        let parts = name.split(separator: " ")
        if parts.count >= 2 {
            return String(parts[0].prefix(1) + parts[1].prefix(1))
        }
        return String(name.prefix(2))
    }
}

// MARK: - Lanyard Shape

struct LanyardShape: Shape {
    func path(in rect: CGRect) -> Path {
        var path = Path()
        let mid = rect.midX
        let top = rect.minY
        let bottom = rect.maxY

        path.move(to: CGPoint(x: mid - 30, y: top))
        path.addQuadCurve(
            to: CGPoint(x: mid, y: bottom),
            control: CGPoint(x: mid - 50, y: rect.midY + 10)
        )
        path.move(to: CGPoint(x: mid + 30, y: top))
        path.addQuadCurve(
            to: CGPoint(x: mid, y: bottom),
            control: CGPoint(x: mid + 50, y: rect.midY + 10)
        )

        return path
    }
}

#Preview {
    let doc = DocumentGenerator.generate(
        identity: Identity(name: "John Smith", organisation: "Torchwood", title: "Agent"),
        documentType: .press_pass
    )
    return PaperView(document: doc)
        .preferredColorScheme(.dark)
        .background(Color(red: 0.04, green: 0.04, blue: 0.04))
}
