# DIY Spectrometer

A Python-based spectroscopy application that uses computer vision to analyze light spectra and identify chemical elements. This tool provides a graphical interface for capturing, analyzing, and comparing spectral data from images or live camera feeds.

## Features

- **Live Camera Capture**: Real-time video feed for spectrum analysis
- **ROI Selection**: Select regions of interest for focused spectral analysis
- **Spectral Analysis**: Extract and visualize RGB intensity distributions
- **Element Identification**: Compare captured spectra against reference patterns for Hydrogen, Helium, and Oxygen
- **Image Processing**: Load and analyze existing spectrum images
- **Data Visualization**: Generate and save spectral plots with matplotlib integration

## Screenshots

The application provides:
- Live camera feed with ROI selection
- Spectral intensity graphs (RGB + mean channels)
- Element identification with confidence levels
- Interactive matplotlib plots with zoom/pan capabilities

## Requirements

```
opencv-python
numpy
matplotlib
tkinter (usually included with Python)
Pillow (PIL)
```

## Installation

1. Clone this repository:
```bash
git clone https://github.com/yourusername/diy-spectrometer.git
cd diy-spectrometer
```

2. Install required dependencies:
```bash
pip install opencv-python numpy matplotlib pillow
```

3. Run the application:
```bash
python spectrometer.py
```

## Usage

### Basic Spectral Analysis

1. **Start Capture**: Click "Start" to begin camera capture
2. **Select ROI**: Press 'R' key to select a region of interest in the video feed
3. **Capture Spectrum**: Press 'S' key to analyze the selected region and generate spectral plots
4. **Save Results**: Enter a filename to save the spectral graph as PNG

### Element Identification

1. **Load Spectrum**: Use "Load Spectrum" button to import an existing spectral image
2. **Analyze**: Click "Find Element" to compare against reference spectra
3. **Results**: View identification results with confidence levels

### Keyboard Controls

- **'R'**: Select Region of Interest (ROI)
- **'S'**: Save/analyze current ROI and generate spectral plot
- **'Q'**: Quit camera capture mode

## Reference Spectra

The application includes basic reference patterns for:
- **Hydrogen**: Characteristic emission lines
- **Helium**: Noble gas spectrum pattern  
- **Oxygen**: Molecular absorption features

*Note: Reference spectra are simplified approximations for demonstration purposes.*

## Technical Details

### Spectral Processing
- Extracts RGB color channels from selected image regions
- Calculates mean intensity distributions across the spectrum
- Compares intensity patterns using absolute difference metrics

### Analysis Methods
- **Template Matching**: Compares captured spectra against known reference patterns
- **Intensity Distribution**: Analyzes color channel variations across the spectral range
- **Confidence Scoring**: Provides uncertainty estimates for element identification

## Output Files

- **Spectral Plots**: PNG files containing RGB intensity graphs
- **Analysis Results**: Element identification with confidence levels displayed in GUI

## Limitations

- Reference spectra are simplified approximations
- Limited to three pre-defined elements (H, He, O)
- Requires good lighting conditions and stable camera setup
- Best results with actual spectroscopy hardware (diffraction grating, etc.)

## Educational Purpose

This project was developed as part of:
**Attività Professionalizzante - 05/2023 - Università di Bologna**

Designed for educational demonstration of spectroscopy principles using accessible computer vision techniques.

## Future Improvements

- [ ] Expand reference spectrum database
- [ ] Implement wavelength calibration
- [ ] Add support for more sophisticated analysis algorithms
- [ ] Include spectral line detection
- [ ] Improve GUI design and user experience

## Contributing

Contributions are welcome! Please feel free to submit pull requests or open issues for bugs and feature requests.

## License

[Add your chosen license here]

## Acknowledgments

- Università di Bologna - Attività Professionalizzante program
- OpenCV community for computer vision tools
- Matplotlib for data visualization capabilities
