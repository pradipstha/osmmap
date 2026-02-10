# City Transport Map Generator - Streamlit App

A web application that generates beautiful city transport maps using OpenStreetMap data.

## 🚀 Quick Start

### Local Installation

1. **Clone or download this repository**

2. **Install dependencies:**
```bash
pip install -r requirements.txt
```

3. **Run the app:**
```bash
streamlit run city_map_app.py
```

4. **Open your browser** to `http://localhost:8501`

## 🌐 Deploy to Streamlit Cloud (FREE)

### Step-by-Step Deployment:

1. **Create a GitHub account** (if you don't have one)
   - Go to https://github.com
   - Sign up for free

2. **Create a new repository**
   - Click "New repository"
   - Name it: `city-map-generator`
   - Make it Public
   - Don't initialize with README

3. **Upload your files to GitHub**

   **Option A: Using GitHub Web Interface (Easiest)**
   - Click "uploading an existing file"
   - Drag and drop all these files:
     - `city_map_app.py`
     - `requirements.txt`
     - `.streamlit/config.toml`
     - `README.md`
   - Click "Commit changes"

   **Option B: Using Git Command Line**
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   git remote add origin https://github.com/YOUR_USERNAME/city-map-generator.git
   git push -u origin main
   ```

4. **Deploy on Streamlit Cloud**
   - Go to https://streamlit.io/cloud
   - Click "Sign up" and use your GitHub account
   - Click "New app"
   - Select your repository: `city-map-generator`
   - Main file path: `city_map_app.py`
   - Click "Deploy"

5. **Wait 5-10 minutes** for deployment to complete

6. **Share your app!** You'll get a URL like:
   `https://YOUR_USERNAME-city-map-generator.streamlit.app`

## 📋 Features

- ✅ **Global Coverage**: Generate maps for any city worldwide
- ✅ **Multiple Network Types**: Drive, bike, and walking paths
- ✅ **Intelligent Caching**: Fast regeneration of previously created maps
- ✅ **High Resolution**: Export maps up to 600 DPI
- ✅ **Error Handling**: Comprehensive error checking and user feedback
- ✅ **Responsive Design**: Works on desktop and mobile
- ✅ **Free to Use**: Open source and completely free

## 🎯 Use Cases

- **Urban Planning**: Analyze transportation network density
- **Research**: Study city morphology and street patterns
- **Art & Design**: Create unique city map posters
- **Real Estate**: Visualize neighborhood connectivity
- **Education**: Teaching urban geography and GIS
- **Travel**: Explore city layouts before visiting

## 🛠️ Technical Details

### Technologies Used:
- **Streamlit**: Web framework
- **OSMnx**: OpenStreetMap data extraction
- **GeoPandas**: Geospatial data processing
- **NetworkX**: Graph analysis
- **Matplotlib**: Visualization

### Performance Optimizations:
- **Geocoding Cache**: 24-hour TTL (time-to-live)
- **Buffer Cache**: 1-hour TTL
- **Network Data Cache**: 1-hour TTL
- **Efficient Memory Management**: Figures closed after display

### Error Handling:
- City not found detection
- Network download failures
- Invalid input validation
- Timeout management
- Memory optimization for large cities

## ⚙️ Configuration Options

### In the Sidebar:
- **City Name**: Any city worldwide (include country for best results)
- **Map Radius**: 5-50 km around city center
- **Coordinate System**: Choose appropriate CRS for your region
- **Network Types**: Drive, bike, walk (select multiple)
- **Image Quality**: 72-600 DPI

### Recommended Settings by Use Case:

**For Printing (Poster):**
- Radius: 10-15 km
- DPI: 300-600
- Networks: Drive + Bike

**For Quick Preview:**
- Radius: 5-10 km
- DPI: 72-150
- Networks: Drive only

**For Detailed Analysis:**
- Radius: 5 km
- DPI: 300
- Networks: All types

## 🐛 Troubleshooting

### Common Issues:

**"City not found"**
- Solution: Add country/state (e.g., "Springfield, Illinois, USA")

**"Taking too long"**
- Solution: Reduce map radius or try during off-peak hours
- Large cities (>30km radius) may take 2-3 minutes

**"No networks downloaded"**
- Solution: City may have limited OSM data
- Try a nearby larger city or different network type

**"Out of memory"**
- Solution: Reduce radius to <20 km
- Close other browser tabs

### Performance Tips:
1. Start with small radius (5-10 km)
2. Use caching - regenerating same city is instant
3. Popular cities cache faster due to OSM optimization
4. Lower DPI for testing, increase for final export

## 📊 Example Cities to Try

### North America:
- New York, New York, USA
- San Francisco, California, USA
- Mexico City, Mexico
- Toronto, Ontario, Canada

### Europe:
- Paris, France
- Barcelona, Spain
- Amsterdam, Netherlands
- Rome, Italy

### Asia:
- Tokyo, Japan
- Singapore
- Bangkok, Thailand
- Seoul, South Korea

### Other:
- Sydney, Australia
- São Paulo, Brazil
- Cairo, Egypt
- Cape Town, South Africa

## 🔒 Privacy & Data

- **No data collection**: App doesn't store any user data
- **Caching**: Local cache only (not shared between users)
- **OpenStreetMap**: All map data from OSM (ODbL license)
- **No API keys needed**: Completely open and free

## 📝 License

This application uses OpenStreetMap data, which is © OpenStreetMap contributors and available under the Open Database License (ODbL).

The application code is open source and free to use.

## 🤝 Credits

- **OpenStreetMap**: Map data
- **OSMnx**: Geoff Boeing
- **Lato Font**: Łukasz Dziedzic

## 💡 Tips for Best Results

1. **Be Specific**: "Paris, France" > "Paris"
2. **Start Small**: Test with 5km radius first
3. **Multiple Networks**: Combine drive + bike for rich maps
4. **Right CRS**: Choose CRS matching your region for accurate buffering
5. **DPI Choice**: 150 DPI is perfect for most uses
6. **Cache Benefit**: Same city regenerates instantly

## 📞 Support

If you encounter issues:
1. Check the troubleshooting section
2. Try with example cities first
3. Verify internet connection
4. Clear browser cache

## 🔄 Updates

To update the app:
1. Pull latest code from repository
2. Update requirements: `pip install -r requirements.txt --upgrade`
3. Restart Streamlit

---

**Made with ❤️ using Streamlit and OpenStreetMap**
