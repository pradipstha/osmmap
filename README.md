# City Transport Map Generator - Streamlit App

A web application that generates city transport maps using OpenStreetMap data.

## 📋 Features

- ✅ **Global Coverage**: Generate maps for any city worldwide
- ✅ **Multiple Network Types**: Drive, bike, and walking paths
- ✅ **High Resolution**: Export maps up to 600 DPI
- ✅ **Free to Use**: Open source and completely free

### Technologies Used:
- **Streamlit**: Web framework
- **OSMnx**: OpenStreetMap data extraction
- **GeoPandas**: Geospatial data processing
- **NetworkX**: Graph analysis
- **Matplotlib**: Visualization

### In the Sidebar:
- **City Name**: Any city worldwide (include country for best results)
- **Map Radius**: 5-50 km around city center
- **Coordinate System**: Choose appropriate CRS for your region
- **Network Types**: Drive, bike, walk (select multiple)
- **Image Quality**: 72-600 DPI

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

---

**Made with ❤️ using Streamlit and OpenStreetMap**
