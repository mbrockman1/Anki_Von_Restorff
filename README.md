# Anki Von Restorff Add-on

The Von Restorff add-on enhances your Anki experience by applying the Von Restorff effect, making specific cards or notes visually distinct to improve memorability. It highlights a randomly selected card or note every X reviews with a customizable style, such as a colorful "goofy" appearance or an inverted (dark) theme.

## Features

- **Customizable Styles**:
  - **Goofy**: User-defined background color, font color, and font type (e.g., Arial, Comic Sans MS) using a color picker.
  - **Inverted**: Fixed white text on a dark background for a high-contrast look.
- **Flexible Targeting**: Apply the effect to individual cards or all cards of a note.
- **Configurable Interval**: Choose how often the effect is applied (e.g., every 20 cards).
- **Dynamic UI**: Hides irrelevant customization options (color and font) when the inverted style is selected.
- **Debug Logging**: Optional logs to troubleshoot issues during reviews.

## Installation

1. **Download the Add-on**:
   - Clone this repository or download the ZIP file from GitHub.
   - Ensure you have the `vonrestorff` folder containing `__init__.py`.

2. **Install in Anki**:
   - Locate your Anki add-ons directory:
     - **macOS**: `~/Library/Application Support/Anki2/addons21/`
     - **Windows**: `C:\Users\<YourUser>\AppData\Roaming\Anki2\addons21\`
     - **Linux**: `~/.local/share/Anki2/addons21/`
   - Copy the `vonrestorff` folder to the add-ons directory.
   - If updating, replace the existing `vonrestorff` folder.

3. **Restart Anki**:
   - Close and reopen Anki to load the add-on.

4. **Verify Installation**:
   - Go to `Tools → Von Restorff Settings` in Anki. If the settings dialog opens, the add-on is installed correctly.

## Usage

1. **Configure Settings**:
   - Open `Tools → Von Restorff Settings` in Anki.
   - Adjust the following options:
     - **Interval**: Number of cards between effect applications (e.g., 20).
     - **Style**:
       - **Goofy**: Customize background color, font color, and font type using color pickers and a dropdown.
       - **Inverted**: Uses a fixed dark theme (hides color/font options).
     - **Target**: Apply the effect to a single card or all cards of a note.
     - **Debug Logs**: Enable to troubleshoot issues (logs appear in Anki’s console).
   - Click "Save" to apply changes.

2. **Review Cards**:
   - During reviews, the add-on highlights a randomly selected card or note every Xth card (based on your interval).
   - The effect persists for the selected card/note within the interval and resets at the start of the next interval.

## Example Configuration

- **Interval**: 20
- **Style**: Goofy
- **Goofy Background**: `#FF6347` (tomato red)
- **Goofy Font Color**: `#FFFFFF` (white)
- **Goofy Font**: Comic Sans MS
- **Target**: Card
- **Debug Logs**: Enabled

With this setup, every 20th card will be highlighted with a red background, white text, and Comic Sans MS font, making it stand out.

## Troubleshooting

- **Effect Not Applying**:
  - Ensure the interval isn’t too high (e.g., set to 10 for testing).
  - Check for conflicts with other add-ons (e.g., "More Answer Buttons with colors" or "Review Heatmap"). Temporarily disable them to test.
  - Enable debug logs in settings and review the console for errors.
- **Settings Dialog Errors**:
  - Verify the `vonrestorff` folder contains only `__init__.py` from the latest version.
  - Restart Anki after updating the add-on.
- **Submit Issues**:
  - Open an issue on this GitHub repository with debug logs and a description of the problem.

## Support the Developer

If you find this add-on helpful, consider supporting the developer via Ko-fi:

[![Support on Ko-fi](https://ko-fi.com/img/githubbutton_sm.svg)](https://ko-fi.com/mbrockman1)

## Contributing

Contributions are welcome! To contribute:
1. Fork this repository.
2. Create a feature branch (`git checkout -b feature/YourFeature`).
3. Commit your changes (`git commit -m "Add YourFeature"`).
4. Push to the branch (`git push origin feature/YourFeature`).
5. Open a pull request.

Please include tests and update this README if necessary.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Built for Anki 25.02.4 (Python 3.9.18, Qt 6.6.2, PyQt 6.6.1).
- Inspired by the Von Restorff effect for enhancing memory retention.