import 'dart:convert';
import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;
import 'config.dart';

void main() => runApp(const ShariaEgxApp());

class ShariaEgxApp extends StatelessWidget {
  const ShariaEgxApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'محلل أسهم البورصة المصرية',
      debugShowCheckedModeBanner: false,
      theme: ThemeData(colorScheme: ColorScheme.fromSeed(seedColor: const Color(0xFF2563EB)), useMaterial3: true),
      home: const AnalyzerHome(),
    );
  }
}

class AnalyzerHome extends StatefulWidget {
  const AnalyzerHome({super.key});
  @override
  State<AnalyzerHome> createState() => _AnalyzerHomeState();
}

class _AnalyzerHomeState extends State<AnalyzerHome> {
  final controller = TextEditingController();
  bool loading = false;
  String? error;
  Map<String, dynamic>? result;

  Future<void> analyze() async {
    final symbol = controller.text.trim().toUpperCase();
    if (symbol.isEmpty) {
      setState(() => error = 'اكتب رمز السهم أولاً');
      return;
    }
    setState(() { loading = true; error = null; result = null; });
    try {
      final response = await http.get(Uri.parse('${AppConfig.apiBaseUrl}/api/v1/analysis/$symbol')).timeout(const Duration(seconds: 15));
      if (response.statusCode != 200) throw Exception('تعذر تحليل السهم: ${response.statusCode}');
      setState(() => result = jsonDecode(response.body) as Map<String, dynamic>);
    } catch (e) {
      setState(() => error = 'لم نتمكن من الاتصال بالخادم. تأكد أن الـ Backend يعمل وأن عنوان API صحيح.');
    } finally {
      if (mounted) setState(() => loading = false);
    }
  }

  @override
  void dispose() { controller.dispose(); super.dispose(); }

  @override
  Widget build(BuildContext context) {
    final indicators = result?['indicators'] as Map<String, dynamic>?;
    return Directionality(
      textDirection: TextDirection.rtl,
      child: Scaffold(
        appBar: AppBar(title: const Text('محلل البورصة المصرية')),
        body: ListView(padding: const EdgeInsets.all(16), children: [
          const Text('تحليل فني للأسهم', style: TextStyle(fontSize: 23, fontWeight: FontWeight.bold)),
          const SizedBox(height: 8),
          const Text('نسخة تجريبية تعتمد على بيانات CSV محلية. حالة التوافق الشرعي لا تُستنتج من حركة السعر.'),
          const SizedBox(height: 18),
          TextField(controller: controller, textDirection: TextDirection.ltr, decoration: const InputDecoration(labelText: 'رمز السهم مثل COMI', border: OutlineInputBorder()), onSubmitted: (_) => analyze()),
          const SizedBox(height: 12),
          FilledButton.icon(onPressed: loading ? null : analyze, icon: const Icon(Icons.analytics_outlined), label: Text(loading ? 'جارٍ التحليل...' : 'حلّل السهم')),
          if (error != null) ...[const SizedBox(height: 12), Text(error!, style: const TextStyle(color: Colors.red))],
          if (result != null) ...[
            const SizedBox(height: 20),
            Card(child: Padding(padding: const EdgeInsets.all(16), child: Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
              Text('${result!['symbol']} — ${result!['as_of']}', style: const TextStyle(fontWeight: FontWeight.bold, fontSize: 18)),
              const SizedBox(height: 8), Text('آخر إغلاق: ${result!['close']}'),
              Text('التقييم الفني: ${result!['technical_summary']} (${result!['technical_score']})'),
              const Divider(),
              Text('RSI 14: ${indicators?['rsi14'] ?? 'غير متاح'}'),
              Text('EMA 20: ${indicators?['ema20'] ?? 'غير متاح'}'),
              Text('EMA 50: ${indicators?['ema50'] ?? 'غير متاح'}'),
              Text('MACD: ${indicators?['macd'] ?? 'غير متاح'}'),
              const Divider(),
              const Text('المراجعة الشرعية: غير محددة', style: TextStyle(fontWeight: FontWeight.bold)),
              const Text('المؤشر 33: غير مفعّل حتى توثيق المعادلة والمصدر.'),
            ]))),
          ],
        ]),
      ),
    );
  }
}
