# Claude-Projekt-Prompter
Ein Python Projekt welches es ermöglicht Projekte komplett oder teilweise mit zugehörigen Fragen an die Claude API von Anthropic zu senden

## Funktionen

- Auswahl des Projektpfads zum Durchsuchen der Projektdateien
- Angabe der zu berücksichtigenden Dateiendungen (durch Komma getrennt)
- Auswahl der maximalen Token-Länge für die Claude-API-Anfrage
- Eingabefeld für Fragen oder Aufgaben an Claude
- Anzeige der generierten Antwort von Claude in einem Textfeld
- Speicherung der Einstellungen (Projektpfad, Dateiendungen, maximale Token-Länge, API-Schlüssel) für zukünftige Sitzungen

## Voraussetzungen

- Python 3.x
- `anthropic`-Bibliothek für die Kommunikation mit der Claude-API
- `tkinter`-Bibliothek für die UI

## Installation

1. Klonen Sie dieses Repository auf Ihren lokalen Computer:

   ```
   git clone https://github.com/your-username/claude-projekt-prompter.git
   ```

2. Navigieren Sie in das Projektverzeichnis:

   ```
   cd claude-projekt-prompter
   ```

3. Installieren Sie die erforderlichen Abhängigkeiten:

   ```
   pip install anthropic tk
   ```

## Verwendung

1. Führen Sie das Tool aus:

   ```
   python main.py
   ```

2. Geben Sie den Projektpfad an, indem Sie auf "Durchsuchen" klicken und den gewünschten Ordner auswählen.

3. Geben Sie die zu berücksichtigenden Dateiendungen an (durch Komma getrennt, z.B. ".json").

4. Wählen Sie die maximale Token-Länge für die Claude-API-Anfrage aus (512, 1024, 2048, 4096).

5. Geben Sie Ihren API-Schlüssel ein.

6. Geben Sie Ihre Frage oder Aufgabe in das Textfeld ein.

7. Klicken Sie auf "Senden", um die Anfrage an die Claude-API zu senden.

8. Die generierte Antwort von Claude wird im Ausgabebereich angezeigt.

9. Die eingegebenen Informationen (Projektpfad, Dateiendungen, maximale Token-Länge, API-Schlüssel) werden automatisch für zukünftige Sitzungen gespeichert.

## Lizenz

Dieses Projekt steht unter der [MIT-Lizenz](LICENSE).
