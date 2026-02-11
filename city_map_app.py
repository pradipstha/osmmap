import streamlit as st
import osmnx as ox
import geopandas as gpd
from geopy.geocoders import Nominatim
from functools import partial
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import networkx as nx
import io
import urllib.request
import os
from pathlib import Path
import time
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Page configuration
st.set_page_config(
    page_title="City Transport Map Generator",
    page_icon="🗺️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
    <style>
    .main {
        padding: 0rem 1rem;
    }
    .stButton>button {
        width: 100%;
        background-color: #FF4B4B;
        color: white;
        font-weight: bold;
        border-radius: 5px;
        padding: 0.5rem 1rem;
        border: none;
    }
    .stButton>button:hover {
        background-color: #FF6B6B;
    }
    .success-box {
        padding: 1rem;
        border-radius: 0.5rem;
        background-color: #D4EDDA;
        border: 1px solid #C3E6CB;
        color: #155724;
        margin: 1rem 0;
    }
    .info-box {
        padding: 1rem;
        border-radius: 0.5rem;
        background-color: #D1ECF1;
        border: 1px solid #BEE5EB;
        color: #0C5460;
        margin: 1rem 0;
    }
    </style>
    """, unsafe_allow_html=True)

# Download and cache font
@st.cache_resource
def load_custom_font():
    """Download and load Lato font"""
    try:
        font_url = "https://github.com/google/fonts/raw/main/ofl/lato/Lato-Regular.ttf"
        font_path = "Lato-Regular.ttf"

        if not os.path.exists(font_path):
            urllib.request.urlretrieve(font_url, font_path)
            logger.info("Font downloaded successfully")

        font_prop = fm.FontProperties(fname=font_path)
        return font_prop
    except Exception as e:
        logger.warning(f"Could not load custom font: {e}")
        return None

# Geocode city with caching
@st.cache_data(ttl=86400)  # Cache for 24 hours
def geocode_city(city_name, timeout=10):
    """
    Geocode a city name to coordinates with error handling
    
    Args:
        city_name: Name of the city
        timeout: Request timeout in seconds
    
    Returns:
        tuple: (success, location_or_error_message)
    """
    try:
        # Use Nominatim with better configuration
        geolocator = Nominatim(
            user_agent="city_transport_map_app_v2",
            timeout=timeout,
            domain='nominatim.openstreetmap.org',
            scheme='https'
        )
        
        # Add retry logic
        import time
        max_retries = 3
        for attempt in range(max_retries):
            try:
                location = geolocator.geocode(
                    city_name,
                    language="en",
                    addressdetails=True
                )
                
                if location is None:
                    return False, f"City '{city_name}' not found. Try adding state/country (e.g., 'Paris, France')"
                
                logger.info(f"Successfully geocoded: {city_name} -> {location.address}")
                return True, location
                
            except Exception as e:
                if attempt < max_retries - 1:
                    time.sleep(2)  # Wait 2 seconds before retry
                    continue
                else:
                    raise e
        
    except Exception as e:
        error_msg = str(e)
        logger.error(f"Geocoding error: {error_msg}")
        
        # Provide helpful error messages
        if "timed out" in error_msg.lower():
            return False, "Geocoding service timed out. Please try again."
        elif "connection" in error_msg.lower():
            return False, "Cannot connect to geocoding service. Please try again in a moment."
        elif "rate" in error_msg.lower() or "limit" in error_msg.lower():
            return False, "Too many requests. Please wait a minute and try again."
        else:
            return False, f"Geocoding error: {error_msg}"


# Create buffer around city with caching
@st.cache_data(ttl=3600)  # Cache for 1 hour
def create_city_buffer(latitude, longitude, buffer_meters, crs_code):
    """
    Create a buffered area around city coordinates

    Args:
        latitude: City latitude
        longitude: City longitude
        buffer_meters: Buffer radius in meters
        crs_code: Coordinate reference system EPSG code

    Returns:
        tuple: (success, geodataframe_or_error_message)
    """
    try:
        # Create GeoDataFrame from coordinates
        cities_df = gpd.GeoDataFrame(
            {'geometry': [gpd.points_from_xy([longitude], [latitude])[0]]},
            crs='EPSG:4326'
        )

        # Transform to specified CRS for accurate buffering
        cities_df = cities_df.to_crs(epsg=crs_code)
        cities_df['buffer'] = cities_df.geometry.buffer(buffer_meters)
        cities_df = cities_df.set_geometry('buffer')

        # Transform back to WGS84 for OSM queries
        cities_df = cities_df.to_crs(epsg=4326)

        logger.info(f"Buffer created: {buffer_meters}m radius")
        return True, cities_df

    except Exception as e:
        logger.error(f"Buffer creation error: {str(e)}")
        return False, f"Error creating buffer: {str(e)}"

# Download OSM network data with caching
@st.cache_data(ttl=3600, show_spinner=False)  # Cache for 1 hour
def download_osm_network(polygon_wkt, network_type):
    """
    Download OSM network data for given polygon

    Args:
        polygon_wkt: Well-Known Text representation of polygon
        network_type: Type of network ('drive', 'bike', 'walk', 'all')

    Returns:
        tuple: (success, graph_or_error_message)
    """
    try:
        from shapely import wkt
        polygon = wkt.loads(polygon_wkt)

        # Configure OSMnx
        ox.settings.use_cache = True
        ox.settings.log_console = False

        graph = ox.graph_from_polygon(
            polygon, 
            network_type=network_type,
            simplify=True
        )

        logger.info(f"Downloaded {network_type} network: {len(graph.nodes)} nodes, {len(graph.edges)} edges")
        return True, graph

    except Exception as e:
        logger.error(f"Network download error ({network_type}): {str(e)}")
        return False, f"Error downloading {network_type} network: {str(e)}"

# Generate map visualization
def generate_map_image(graph, city_name, network_types, font_prop=None):
    """
    Generate map visualization from network graph

    Args:
        graph: NetworkX graph of street network
        city_name: Name of the city for labeling
        network_types: String describing network types
        font_prop: Font properties for text

    Returns:
        tuple: (success, figure_or_error_message)
    """
    try:
        # Create figure
        fig, ax = ox.plot_graph(
            graph,
            figsize=(20, 20),
            node_size=0,
            edge_color='white',
            edge_linewidth=0.5,
            bgcolor='black',
            show=False,
            close=False
        )
     
        formatted_city_name = city_name.title()

        # Base style
        base_kwargs = {
            'color': 'white',
            'ha': 'center',
            'va': 'bottom',
            'transform': ax.transAxes}
        if font_prop:
            base_kwargs['fontproperties'] = font_prop

        city_kwargs = dict(base_kwargs)
        city_kwargs.update({'fontsize': 30, 'weight': 'bold'})
        network_kwargs = dict(base_kwargs)
        network_kwargs.update({'fontsize': 18})

        # Place at bottom inside axes; minimal gap
        city_y = 0.04
        gap = 0.018 
        network_y = city_y + gap

        ax.text(0.5, city_y, formatted_city_name, **city_kwargs)
        ax.text(0.5, network_y, network_types, **network_kwargs)
        fig.subplots_adjust(top=0.08, bottom=0.98)

        logger.info("Map visualization created successfully")
        return True, fig

    except Exception as e:
        logger.error(f"Map generation error: {str(e)}")
        return False, f"Error generating map: {str(e)}"

# Convert figure to bytes for download
def fig_to_bytes(fig, dpi=250):
    """Convert matplotlib figure to bytes"""
    buf = io.BytesIO()
    fig.savefig(buf, format='png', dpi=dpi, bbox_inches='tight', facecolor='black')
    buf.seek(0)
    return buf

# Main app
def main():
    # Header
    st.title("City Transport Map Generator")
    st.markdown("Generate street network maps from OpenStreetMap data")

    # Sidebar for inputs
    with st.sidebar:
        st.header("⚙️ Map Settings")

        # City input
        city_name = st.text_input(
            "City Name",
            value="College Station, Texas",
            help="Enter city name. Include state/country for better results (e.g., 'Paris, France')"
        )

        # Buffer/radius
        buffer = st.slider(
            "Map Radius (km)",
            min_value=5,
            max_value=50,
            value=15,
            step=1,
            help="Area to include around city center"
        )
        buffer_meters = buffer * 1000

        # CRS selection
        crs_options = {
            "WGS 84 (Global)": 4326,
            "Web Mercator": 3857,
            "Texas State Plane (North Central)": 2277,
            "UTM Zone 10N (West US)": 32610,
            "UTM Zone 33N (Europe)": 32633,
            "UTM Zone 43N (India West/Central)": 32643,
            "UTM Zone 44N (India Central/East)": 32644,
            "UTM Zone 45N (India East/Bangladesh)": 32645,
            "UTM Zone 46N (Bangladesh East)": 32646,
            "UTM Zone 47N (Thailand/Myanmar)": 32647,
            "UTM Zone 48N (Vietnam)": 32648,
            "UTM Zone 51N (Japan/Korea)": 32651,
        }

        crs_choice = st.selectbox(
            "Coordinate System",
            options=list(crs_options.keys()),
            index=2,
            help="Choose appropriate CRS for your region"
        )
        crs = crs_options[crs_choice]

        # Network type selection
        st.markdown("---")
        st.subheader("Network Types")

        include_drive = st.checkbox("🚗 Driving Roads", value=True)
        include_bike = st.checkbox("🚴 Bike Paths", value=True)
        include_walk = st.checkbox("🚶 Walking Paths", value=False)

        if not (include_drive or include_bike or include_walk):
            st.warning("⚠️ Select at least one network type")

        # Resolution
        st.markdown("---")
        dpi = st.select_slider(
            "Image Quality (DPI)",
            options=[72, 150, 300, 600],
            value=150,
            help="Higher DPI = better quality but larger file size"
        )

        st.markdown("---")
        generate_btn = st.button("🚀 Generate Map", type="primary", disabled=not (include_drive or include_bike or include_walk))

        # Info section
        with st.expander("ℹ️ Tips & Info"):
            st.markdown("""
            **Tips for best results:**
            - Include country/state in city name
            - Start with smaller radius for faster results
            - Large cities may take 1-2 minutes

            **Network Types:**
            - **Drive**: All drivable roads
            - **Bike**: Dedicated bike paths and lanes
            - **Walk**: Pedestrian paths and trails

            **Common CRS by Region:**
            - **Global/Unknown**: WGS 84
            - **Web maps**: Web Mercator
            - **Texas**: State Plane 2277
            - **West US**: UTM Zone 10N
            - **Europe**: UTM Zone 33N
            - **India West/Central**: UTM Zone 43N
            - **India East/Bangladesh**: UTM Zone 44N-45N
            """)

    # Main content area

    if generate_btn:
        # Load font
        font_prop = load_custom_font()

        # Progress container
        progress_container = st.container()

        with progress_container:
            progress_bar = st.progress(0)
            status_text = st.empty()

            try:
                # Step 1: Geocode city
                status_text.text("🔍 Finding city location...")
                progress_bar.progress(10)

                success, result = geocode_city(city_name)
                if not success:
                    st.error(f"❌ {result}")
                    st.stop()

                location = result
                st.success(f"✅ Found: {location.address}")
                progress_bar.progress(20)

                # Step 2: Create buffer
                status_text.text("📍 Creating study area...")
                success, result = create_city_buffer(
                    location.latitude,
                    location.longitude,
                    buffer_meters,
                    crs
                )

                if not success:
                    st.error(f"❌ {result}")
                    st.stop()

                cities_df = result
                progress_bar.progress(30)

                # Step 3: Download networks
                polygon_wkt = cities_df.geometry.iloc[0].wkt
                graphs = []
                networks_downloaded = []

                total_networks = sum([include_drive, include_bike, include_walk])
                current_network = 0

                if include_drive:
                    current_network += 1
                    status_text.text(f"⬇️ Downloading driving network ({current_network}/{total_networks})...")
                    success, result = download_osm_network(polygon_wkt, 'drive')

                    if success:
                        graphs.append(result)
                        networks_downloaded.append("Drive")
                        st.success("✅ Drive network downloaded")
                    else:
                        st.warning(f"⚠️ {result}")

                    progress_bar.progress(30 + (current_network * 20))

                if include_bike:
                    current_network += 1
                    status_text.text(f"⬇️ Downloading bike network ({current_network}/{total_networks})...")
                    success, result = download_osm_network(polygon_wkt, 'bike')

                    if success:
                        graphs.append(result)
                        networks_downloaded.append("Bike")
                        st.success("✅ Bike network downloaded")
                    else:
                        st.warning(f"⚠️ {result}")

                    progress_bar.progress(30 + (current_network * 20))

                if include_walk:
                    current_network += 1
                    status_text.text(f"⬇️ Downloading walking network ({current_network}/{total_networks})...")
                    success, result = download_osm_network(polygon_wkt, 'walk')

                    if success:
                        graphs.append(result)
                        networks_downloaded.append("Walk")
                        st.success("✅ Walk network downloaded")
                    else:
                        st.warning(f"⚠️ {result}")

                    progress_bar.progress(30 + (current_network * 20))

                if not graphs:
                    st.error("❌ No networks could be downloaded. Try a different city or smaller radius.")
                    st.stop()

                # Step 4: Combine networks
                status_text.text("🔗 Combining networks...")
                progress_bar.progress(80)

                if len(graphs) > 1:
                    combined_graph = graphs[0]
                    for g in graphs[1:]:
                        combined_graph = nx.compose(combined_graph, g)
                else:
                    combined_graph = graphs[0]

                # Network statistics
                st.info(f"📊 Network contains {len(combined_graph.nodes):,} nodes and {len(combined_graph.edges):,} edges")

                # Step 5: Generate map
                status_text.text("Creating visualization...")
                progress_bar.progress(90)

                # Create network types label
                network_label = " and ".join(networks_downloaded)
                
                success, result = generate_map_image(combined_graph, city_name, network_label, font_prop)

                if not success:
                    st.error(f"❌ {result}")
                    st.stop()

                fig = result
                progress_bar.progress(100)
                status_text.text("✅ Map generated successfully!")
                time.sleep(0.5)

                # Clear progress indicators
                progress_container.empty()

                # Display map
                st.success(f"🎉 Map of {city_name} generated successfully!")
                st.markdown(f"**Networks included:** {', '.join(networks_downloaded)}")

                st.pyplot(fig)

                # Download button
                filename = f"{city_name.replace(' ', '_').replace(',', '')}_transport_map.png"
                img_bytes = fig_to_bytes(fig, dpi=dpi)

                st.download_button(
                    label=f"📥 Download Map (PNG, {dpi} DPI)",
                    data=img_bytes,
                    file_name=filename,
                    mime="image/png",
                    type="primary"
                )

                # Close figure to free memory
                plt.close(fig)

            except Exception as e:
                logger.error(f"Unexpected error: {str(e)}")
                st.error(f"❌ An unexpected error occurred: {str(e)}")
                st.info("💡 Try reducing the map radius or choosing a different city")

    else:
        # Show welcome message when no map generated
        st.info(" Configure your map settings in the sidebar and click 'Generate Map' to begin")

        st.markdown("---")
        st.subheader("")

        col_a, col_b = st.columns(2)

if __name__ == "__main__":
    main()
