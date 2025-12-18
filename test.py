import os
from core.voice_analysis_service import VoiceAnalysisService
from core.db_manager import TinyDBVoiceManager


def test_accuracy():
    """Тестирование точности распознавания"""
    analyzer = VoiceAnalysisService()
    db = TinyDBVoiceManager()

    # Получаем всех людей из базы
    all_people = db.get_all_people()

    print("=== ТЕСТИРОВАНИЕ ТОЧНОСТИ ===\n")

    results = []

    for person in all_people:
        person_name = person['full_name']
        audio_files = person['audio_files']

        print(f"🧪 Тестируем: {person_name}")
        print(f"   Файлов для теста: {len(audio_files)}")

        correct = 0
        total = 0

        for audio_file in audio_files:
            if os.path.exists(audio_file):
                result = analyzer.analyze(audio_file)
                total += 1

                if result["status"] == "ok":
                    if result["best_match"]["person"]["full_name"] == person_name:
                        correct += 1
                        print(f"   ✅ {os.path.basename(audio_file)}: правильно")
                    else:
                        print(f"   ❌ {os.path.basename(audio_file)}: ошибка")
                else:
                    print(f"   ⚠️  {os.path.basename(audio_file)}: не распознан")

        if total > 0:
            accuracy = correct / total * 100
            results.append((person_name, accuracy))
            print(f"   📊 Точность: {accuracy:.1f}% ({correct}/{total})\n")

    # Общая статистика
    if results:
        print("\n=== ОБЩАЯ СТАТИСТИКА ===")
        for name, acc in results:
            print(f"{name}: {acc:.1f}%")

        avg_accuracy = sum(acc for _, acc in results) / len(results)
        print(f"\n🎯 Средняя точность: {avg_accuracy:.1f}%")


if __name__ == "__main__":
    test_accuracy()