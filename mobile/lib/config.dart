class AppConfig {
  // Android emulator can reach the host machine at 10.0.2.2.
  // Change this for a physical device or deployed backend.
  static const String apiBaseUrl = String.fromEnvironment(
    'API_BASE_URL',
    defaultValue: 'http://10.0.2.2:8000',
  );
}
