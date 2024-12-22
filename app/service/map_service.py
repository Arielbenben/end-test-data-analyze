import folium



def add_a_marker_to_map(map_object, lat: float, lot: float, popup_name: str, content, color: str = None):
    icon = folium.Icon(color=color) if color else None
    folium.Marker(
        location=[lat, lot],
        popup=f"<b>{popup_name}:</b><br>{content}",
        tooltip=f"Click to view {popup_name}",
        icon=icon
    ).add_to(map_object)
    return map_object


def create_map_object():
    return folium.Map(location=[31.9686, 34.7805], zoom_start=3)

