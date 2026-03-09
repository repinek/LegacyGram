# LegacyGram Plugin
A highly customizable plugin for [exteraGram](https://exteragram.app) based clients to **remove paid and bloated features** from the Android Telegram client 

**Recommended version:** `12.1.1`

## Screenshots & Features

|                                    |                                    |                                    |
|:----------------------------------:|:----------------------------------:|:----------------------------------:|
| ![preview_1](images/preview_1.png) | ![preview_2](images/preview_2.png) | ![preview_3](images/preview_3.png) |


## Building
1. Clone the repo:
```bash
git clone https://github.com/repinek/LegacyGram.git
cd LegacyGram
```
2. Install dependencies using [uv](https://docs.astral.sh/uv/):
```bash
uv sync
```
3. Build
```bash
uv run build.py
```
Result of building will be saved at `dist/LegacyGram.plugin`

## Installation
1. Send `LegacyGram.plugin` to any Telegram chat (e.g., **Saved Messages**).
2. Tap on the file in the chat and tap **Install**.

## Debugging & Development
Refer to the [exteraGram plugins documentation](https://plugins.exteragram.app/docs/setup)

Also Project includes a `typings/` directory with typings stubs for `android`, `xposed`, `java` and `Chaquopy Python API` 

## Contributing 
Pull requests are welcome!

## Project Structure
```
├── LegacyGram/
│   ├── main.py                 # Entry Point
│   ├── data/                   # Constants
│   ├── features/               # Features by categories
│   ├── i18n/                   # Internationalization system
│   │   └── locales.py          # Localization
│   ├── ui/                     # Settings UI
│   └── utils/                  # Helper functions
│
├── typings/                    # Typings stubs for java, xposed and android
│   ├── android/
│   │   └── view/               
│   ├── de/
│   │   └── robv/
│   │       └── android/
│   │           └── xposed/
│   └── java/
│       └── lang/
│           └── reflect/
│
├── build.py                    # Plugin Build Script
├── pyproject.toml              # Project Configuration File
└── uv.lock                     # lockfile for uv
```

## License 
This project is licensed under the **MIT License**.  
See the [LICENSE](LICENSE) file for details.

## Acknowledgements
exteraGram Team - For wonderful [Telegram fork](https://exteragram.app) and [Plugin System](https://plugins.exteragram.app/)  
[Xposed Hooks](https://github.com/LSPosed/LSPosed/blob/master/core/src/main/java/de/robv/android/xposed/XC_MethodHook.java)
