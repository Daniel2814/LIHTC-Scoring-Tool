# LIHTC Location Scoring Tool

A comprehensive web application for calculating location-based scoring criteria for Low-Income Housing Tax Credit (LIHTC) applications in Georgia, based on the 2024-2025 Qualified Allocation Plan (QAP).

Created by **Emory's Center for AI**

## Overview

The LIHTC Location Scoring Tool automates the calculation of location-based criteria that comprise approximately 39% of the total LIHTC application scoring. The tool evaluates potential development sites across four main categories:

- **Desirable/Undesirable Activities** (±20 points)
- **Community Transportation Options** (6 points)
- **Quality Education Areas** (3 points)
- **Stable Communities** (10 points)

## Features

### 🎯 Core Functionality
- **Interactive Map Interface** - Visualize scoring data across Georgia
- **Coordinate-Based Scoring** - Input latitude/longitude for precise location analysis
- **Real-Time Calculations** - Instant scoring updates as you adjust parameters
- **Multi-Site Comparison** - Compare multiple potential development locations

### 📊 Scoring Categories
- **Transportation Analysis** - Transit-oriented development and fixed-route access scoring
- **Community Amenities** - Proximity to grocery stores, healthcare, parks, and services
- **Education Quality** - School performance ratings and attendance zone analysis
- **Community Stability** - Socioeconomic indicators and environmental health metrics

### 🎨 User Experience
- **Dark/Light Mode Toggle** - Customizable interface themes
- **Professional Design** - Clean, accessible interface optimized for professional use
- **Responsive Layout** - Works on desktop, tablet, and mobile devices
- **Comprehensive Documentation** - Built-in QAP reference and scoring criteria

## Installation

### Prerequisites
- Python 3.8 or higher
- pip package manager

### Setup
1. **Clone the repository:**
   ```bash
   git clone https://github.com/YOUR_USERNAME/LIHTC-Scoring-Tool.git
   cd LIHTC-Scoring-Tool
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application:**
   ```bash
   streamlit run scoring_tool.py
   ```

4. **Access the application:**
   Open your browser to `http://localhost:8501`

## Usage

### Basic Workflow

1. **Enter Location Coordinates**
   - Input latitude and longitude for your proposed development site
   - Use the map interface to verify location accuracy

2. **Review Automated Scoring**
   - View calculated scores for all four location-based criteria
   - Examine detailed breakdowns for each scoring category

3. **Analyze Results**
   - Compare scores against QAP thresholds
   - Identify opportunities for site optimization
   - Export results for application documentation

### Navigation

The application includes three main sections:

- **Scoring Tool** (Main Page) - Interactive scoring interface and map visualization
- **QAP Criteria** - Complete reference of all LIHTC scoring categories
- **QAP Documentation** - Full QAP 2024-2025 document viewer

## Technical Architecture

### Built With
- **Streamlit** - Web application framework
- **GeoPandas** - Geospatial data processing
- **Folium** - Interactive map visualization
- **Pandas** - Data manipulation and analysis

### Data Sources
- Georgia Department of Community Affairs (DCA) datasets
- U.S. Census Bureau demographic data
- Georgia Department of Education school performance data
- GTFS transit data for transportation analysis

### Key Components
```
LIHTC-Scoring-Tool/
├── scoring_tool.py              # Main application interface
├── aggregate_scoring.py         # Core scoring algorithms
├── pages/
│   ├── QAP_Criteria.py         # Scoring criteria reference
│   └── QAP_Documentation.py    # QAP document viewer
├── map_layers/
│   ├── build_layers.py         # Map layer construction
│   └── colours.py              # Map styling and colors
└── data/                       # Geospatial datasets
```

## Scoring Methodology

### Location-Based Criteria (39 points total)

| Category | Points | Description |
|----------|--------|-------------|
| Desirable/Undesirable Activities | ±20 | Proximity to amenities vs. hazards |
| Community Transportation | 6 | Transit access and TOD proximity |
| Quality Education | 3 | School performance in attendance zones |
| Stable Communities | 10 | Socioeconomic and environmental indicators |

### Complete QAP Scoring Overview

The tool focuses on location-based criteria within the broader QAP scoring framework:

- **Total Standard Points:** ~99 points for new construction
- **Location Impact:** 39.4% of total possible score
- **Application Types:** New construction, rehabilitation, and preservation

## Contributing

We welcome contributions to improve the LIHTC Scoring Tool:

1. **Fork the repository**
2. **Create a feature branch** (`git checkout -b feature/improvement`)
3. **Commit your changes** (`git commit -am 'Add new feature'`)
4. **Push to the branch** (`git push origin feature/improvement`)
5. **Create a Pull Request**

### Development Guidelines
- Follow existing code style and documentation patterns
- Test changes thoroughly before submitting
- Update documentation for new features
- Ensure compatibility with current data sources

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- **Georgia Department of Community Affairs** - QAP framework and data sources
- **Emory University Center for AI** - Project development and research
- **Streamlit Community** - Open-source web framework

## Contact

For questions, support, or collaboration opportunities:

- **Project Repository:** [GitHub Repository URL]
- **Issues:** Report bugs or request features via GitHub Issues
- **Documentation:** Complete QAP 2024-2025 available within the application

## Disclaimer

This tool is designed to assist with LIHTC application preparation but does not guarantee scoring accuracy. Users should verify all calculations against the official QAP 2024-2025 document and consult with qualified professionals for application submission.

---

**Version:** 1.0.0  
**Last Updated:** January 2025  
**QAP Version:** 2024-2025 Georgia DCA Qualified Allocation Plan