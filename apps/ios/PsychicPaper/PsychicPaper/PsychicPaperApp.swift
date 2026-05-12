import SwiftUI

@main
struct PsychicPaperApp: App {
    @AppStorage("hasCompletedSetup") private var hasCompletedSetup = false

    var body: some Scene {
        WindowGroup {
            if hasCompletedSetup {
                ContentView()
                    .preferredColorScheme(.dark)
            } else {
                SetupView()
                    .preferredColorScheme(.dark)
            }
        }
    }
}
