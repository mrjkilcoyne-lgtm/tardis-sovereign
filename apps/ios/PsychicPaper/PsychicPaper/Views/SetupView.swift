import SwiftUI

struct SetupView: View {
    @AppStorage("hasCompletedSetup") private var hasCompletedSetup = false

    @State private var name = ""
    @State private var organisation = ""
    @State private var title = ""
    @State private var currentStep = 0
    @State private var shimmerOffset: CGFloat = -200

    private let steps = ["Name", "Organisation", "Title"]

    var body: some View {
        ZStack {
            Color(red: 0.04, green: 0.04, blue: 0.04)
                .ignoresSafeArea()

            VStack(spacing: 40) {
                Spacer()

                // Header
                VStack(spacing: 12) {
                    Image(systemName: "doc.viewfinder")
                        .font(.system(size: 48, weight: .thin))
                        .foregroundStyle(
                            LinearGradient(
                                colors: [.white, .white.opacity(0.5)],
                                startPoint: .top,
                                endPoint: .bottom
                            )
                        )

                    Text("Psychic Paper")
                        .font(.system(size: 32, weight: .ultraLight, design: .default))
                        .foregroundColor(.white)
                        .tracking(4)

                    Text("It shows them whatever I want them to see.")
                        .font(.system(size: 14, weight: .light))
                        .foregroundColor(.white.opacity(0.4))
                        .italic()
                }

                // Step indicator
                HStack(spacing: 8) {
                    ForEach(0..<3) { i in
                        Capsule()
                            .fill(i <= currentStep ? Color.white : Color.white.opacity(0.15))
                            .frame(width: i == currentStep ? 28 : 8, height: 4)
                            .animation(.easeInOut(duration: 0.3), value: currentStep)
                    }
                }

                // Input area
                VStack(spacing: 24) {
                    Text(promptForStep)
                        .font(.system(size: 14, weight: .medium))
                        .foregroundColor(.white.opacity(0.5))
                        .tracking(2)
                        .textCase(.uppercase)
                        .animation(.easeInOut, value: currentStep)

                    Group {
                        switch currentStep {
                        case 0:
                            fieldInput(text: $name, placeholder: "John Smith")
                        case 1:
                            fieldInput(text: $organisation, placeholder: "Torchwood Institute")
                        default:
                            fieldInput(text: $title, placeholder: "Consultant")
                        }
                    }
                    .transition(.asymmetric(
                        insertion: .move(edge: .trailing).combined(with: .opacity),
                        removal: .move(edge: .leading).combined(with: .opacity)
                    ))
                }
                .padding(.horizontal, 32)

                Spacer()

                // Navigation
                HStack(spacing: 20) {
                    if currentStep > 0 {
                        Button {
                            withAnimation(.easeInOut(duration: 0.3)) {
                                currentStep -= 1
                            }
                        } label: {
                            Image(systemName: "chevron.left")
                                .font(.system(size: 16, weight: .medium))
                                .foregroundColor(.white.opacity(0.5))
                                .frame(width: 50, height: 50)
                                .background(Color.white.opacity(0.05))
                                .clipShape(Circle())
                        }
                    }

                    Button {
                        advance()
                    } label: {
                        HStack(spacing: 8) {
                            Text(currentStep == 2 ? "Begin" : "Next")
                                .font(.system(size: 16, weight: .medium))
                                .tracking(1)

                            Image(systemName: currentStep == 2 ? "sparkles" : "chevron.right")
                                .font(.system(size: 14, weight: .medium))
                        }
                        .foregroundColor(.black)
                        .frame(maxWidth: .infinity)
                        .frame(height: 50)
                        .background(
                            canAdvance
                                ? AnyShapeStyle(Color.white)
                                : AnyShapeStyle(Color.white.opacity(0.15))
                        )
                        .clipShape(Capsule())
                    }
                    .disabled(!canAdvance)
                }
                .padding(.horizontal, 32)
                .padding(.bottom, 40)
            }
        }
    }

    // MARK: - Subviews

    private func fieldInput(text: Binding<String>, placeholder: String) -> some View {
        TextField("", text: text, prompt: Text(placeholder).foregroundColor(.white.opacity(0.2)))
            .font(.system(size: 24, weight: .light))
            .foregroundColor(.white)
            .multilineTextAlignment(.center)
            .textInputAutocapitalization(.words)
            .autocorrectionDisabled()
            .padding(.vertical, 16)
            .overlay(
                Rectangle()
                    .fill(Color.white.opacity(0.1))
                    .frame(height: 1),
                alignment: .bottom
            )
    }

    // MARK: - Logic

    private var promptForStep: String {
        switch currentStep {
        case 0: return "Your Name"
        case 1: return "Organisation"
        default: return "Title / Role"
        }
    }

    private var canAdvance: Bool {
        switch currentStep {
        case 0: return !name.trimmingCharacters(in: .whitespaces).isEmpty
        default: return true
        }
    }

    private func advance() {
        if currentStep < 2 {
            withAnimation(.easeInOut(duration: 0.3)) {
                currentStep += 1
            }
        } else {
            let identity = Identity(name: name, organisation: organisation, title: title)
            identity.save()
            withAnimation(.easeInOut(duration: 0.5)) {
                hasCompletedSetup = true
            }
        }
    }
}

#Preview {
    SetupView()
        .preferredColorScheme(.dark)
}
