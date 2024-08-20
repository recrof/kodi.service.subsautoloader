# Kodi Addon: Autoload Subtitles from `Subs` Folder

## Overview

This Kodi addon automatically loads subtitles from a `Subs` folder when video playback begins. It supports both movies and TV series, using a folder structure common in most media libraries.

- **Movies:** `Subs/[number]_[language].srt`
- **Series:** `Subs/Name.of.the.video/[number]_[language].srt`

This addon is designed to enhance your viewing experience by seamlessly loading subtitles according to your preferred language settings in Kodi.

## Features

- **Auto-Subtitle Loading:** Automatically loads subtitles for movies and TV series from the `Subs` folder, based on the Kodi preferred subtitle language setting.
- **Multi-Subtitle Support:** Supports loading multiple subtitle files directly from the `Subs` folder or from other configured directories.
- **Configurable Languages:** Ability to configure additional preferred languages using the addon settings, allowing for greater flexibility in subtitle selection.
- **Configurable Default Subs Folder:** Ability to configure the default `Subs` folder using the addon settings.
- **Common Structure Support:** Supports subtitle folder structures commonly used across different media types.

## Configuration

### Folder Structure

- **Movies:** The subtitles should be placed in the `Subs` folder, following this naming convention:
  ```
  Subs/[number]_[language].srt
  ```
  Example: `Subs/01_english.srt`

- **TV Series:** Subtitles for episodes should be placed within the corresponding video folder, like this:
  ```
  Subs/Name.of.the.video/[number]_[language].srt
  ```
  Example: `Subs/Name.of.the.show.S01E01/01_english.srt`

### Language Settings

The `[language]` placeholder refers to the first language configured in Kodi's settings (`Player > Subtitles > Preferred Subtitle Language`). You can also set additional languages within the addon configuration.

## Installation and Usage

### Step 1: Download the Addon

Head over to the [Releases](#) section of this repository and download the latest release of the addon as a `.zip` file.

### Step 2: Install the Addon

Once downloaded, follow the official [Kodi guide to install the addon from a zip file](https://kodi.wiki/view/Archive:Install_add-ons_from_zip_files).

### Step 3: Enjoy Subtitles Autoload

After installation, the subtitle autoload feature should work immediately upon video playback. No additional setup is required for basic functionality.

## Customization

### Multi-Subtitle Loading

If you need to load multiple subtitle files, you can configure this within the addon settings. This allows you to select and load multiple subtitle tracks from either the default `Subs` folder or from other directories that you configure.

### Preferred Languages

The addon lets you configure additional preferred subtitle languages through its settings. This feature is useful for multilingual viewers who prefer subtitles in different languages for various content.

## Troubleshooting

If the addon is not working as expected:
- Ensure that the subtitle files are named and structured correctly.
- Double-check the configured language settings in Kodi (`Player > Subtitles > Preferred Subtitle Language`).
- Automatic scan for `Subs` folder and other possible folders = {`'Subs', 'Sub', 'Subtitles', 'subs', 'sub', 'subtitles'`} placed correctly in relation to your media files.

## Contributing

Contributions are welcome! If you would like to contribute to the development of this addon:
- Fork this repository.
- Make your changes in a new branch.
- Submit a pull request with a detailed description of your changes.

Please ensure that your code adheres to the project's coding standards and that you test your changes thoroughly before submitting.

## License

This project is licensed under the Apache License. See the [LICENSE](LICENSE) file for more details.

