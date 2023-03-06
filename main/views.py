from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def welcome(request):
    return render(request,'main/welcome.html')

def mainfunction(request):
    if request.method == 'POST':
        Source = request.POST['Source']
        Destination = request.POST['Destination']
        Dict_Node = request.POST['Dict_Node']
        D = Dict_Node.split(',')
        D_list = []
        for info in D:
            D_list.append({"start": int(info[0]), "end": int(info[1])})
        import folium
        from folium.plugins import AntPath

        # Define the coordinates of your nodes
        nodes = [
            {"name": "Street 1", "lat": 37.773972, "lon": -122.431297},
            {"name": "Street 2", "lat": 37.772801, "lon": -122.430290},
            {"name": "Street 3", "lat": 37.773382, "lon": -122.428609},
            {"name": "Street 4", "lat": 37.774267, "lon": -122.429259},
            {"name": "Street 5", "lat": 37.778474, "lon": -122.426903},
            {"name": "Street 6", "lat": 37.773383, "lon": -122.428610},
            {"name": "Street 7", "lat": 37.771685, "lon": -122.429230},
            {"name": "Street 8", "lat": 37.773488, "lon": -122.426933},
            {"name": "Street 9", "lat": 37.775399, "lon": -122.428790}
        ]

        # Create a dictionary that maps node numbers to their coordinates
        node_dict = {i+1: (node["lat"], node["lon"]) for i, node in enumerate(nodes)}

        source = Source
        Destination = Destination

        # Get user input for the connections between your nodes
        edges = D_list

        # Create a folium map object centered at a specific location and with a specific zoom level
        map_obj = folium.Map(location=[37.773972, -122.431297], zoom_start=14)

        # Add markers for each node
        for node in nodes:
            folium.Marker(
                location=[node["lat"], node["lon"]],
                tooltip=node["name"],
            ).add_to(map_obj)

        folium.Marker([nodes[0]["lat"],nodes[0]["lon"]],
                    icon=folium.Icon(color='green', prefix='fa',icon='truck')).add_to(map_obj)
        
        truck_icon = folium.features.CustomIcon(icon_image = '/home/sumanth/projects/Personal/mgraph/main/Bike.png',
                                         icon_size=(200, 100))
        truck_marker = folium.Marker(location=node_dict[1], icon=truck_icon)
        truck_marker.add_to(map_obj)
        # Add lines for each edge
        for edge in edges:
            start_node = node_dict[edge["start"]]
            end_node = node_dict[edge["end"]]
            locations = [start_node, end_node]
            
        
            folium.plugins.AntPath(
                locations,
                color='black',
                weight= 10,
                dash_array=[10, 100],
                delay=2000,  # Delay between animation loops (in milliseconds)
                paused=False,  # Whether the animation is paused or not
            ).add_to(map_obj)

        # Save the map to an HTML file
        map_obj.save('main/templates/main/map.html')
        return render(request,'main/map.html')
    else:
        return render(request,'main/takeinput.html')