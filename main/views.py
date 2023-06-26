from django.shortcuts import render
from django.http import HttpResponse



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
        from folium.plugins import PolyLineTextPath
        import math
        import random
        import time

        # Define the coordinates of your nodes
        nodes = [
            {"name": "Street 1", "lat": 17.5076, "lon": 78.4301},
            {"name": "Street 2", "lat": 17.3673, "lon": 78.3744},
            {"name": "Street 3", "lat": 17.3662, "lon": 78.4412},
            {"name": "Street 4", "lat": 17.4011, "lon": 78.5630},
            {"name": "Street 5", "lat": 17.2654, "lon": 78.4301},
            {"name": "Street 6", "lat": 17.1790, "lon": 78.6834},
            {"name": "Street 7", "lat": 17.4532, "lon": 78.9875},
            {"name": "Street 8", "lat": 17.2095, "lon": 78.2301},
        ]

        # Create a dictionary that maps node numbers to their coordinates
        node_dict = {i+1: (node["lat"], node["lon"]) for i, node in enumerate(nodes)}

        source = Source
        Destination = Destination

        # Get user input for the connections between your nodes
        edges = D_list
        print(edges)
    
        # Create a folium map object centered at a specific location and with a specific zoom level
        map_obj = folium.Map(location=[17.4143, 78.4628], zoom_start=14)
        marker = folium.Marker(location=[17.4143, 78.4628],  popup='Hello, world!', auto_open=True)
        marker.add_to(map_obj)
        marker.location = [17.4011, 78.5630]
        marker.popup = 'New Location'
        marker.add_to(map_obj)
       
        # Add markers for each node
        for node in nodes:
            folium.Marker(
                location=[node["lat"], node["lon"]],
                tooltip=node["name"],
            ).add_to(map_obj)

        # folium.Marker([nodes[0]["lat"], nodes[0]["lon"]],
        #       icon=folium.Icon(color='green', prefix='fa', icon='truck')).add_to(map_obj)
        global count
        count = -1
        for i in nodes:
            count +=  1
            if i["name"] == Destination:
                folium.Marker([nodes[count]["lat"],nodes[count]["lon"]],
                    icon=folium.Icon(color='red', prefix='fa',icon='fire')).add_to(map_obj)
        print("len",len(edges))
        count = 0
        min = nodes[0]["lat"]
        distances = []
        for edge in edges:

            count+=1
            start_node = node_dict[edge["start"]]
            end_node = node_dict[edge["end"]]
            locations = [start_node, end_node]
            distance = ((start_node[0] - end_node[0]) ** 2 + (start_node[1] - end_node[1]) ** 2) ** 0.5
            distances.append(distance)
            mid_lat = (start_node[0] + end_node[0]) / 2
            mid_lon = (start_node[1] + end_node[1]) / 2
            mid_point = (mid_lat, mid_lon)

        
                
            polyline = folium.PolyLine(
            locations=locations,
            color='red',
            weight=3,
            opacity=0.7,
            smooth_factor=0.5,
        ).add_to(map_obj)
            
        
            text_label = folium.plugins.PolyLineTextPath(
                polyline=polyline,
                text=str(round(distance, 2)) + ' km',
                weight=0,
                offset=10,
                repeat=False,
                center=True,
                align='center',
                text_color='black',
                font_size=60, 
                opacity=0.7,
            )
            folium.plugins.PolyLineOffset(
                locations=[start_node, mid_point, end_node],
                color='red',
                weight=3,
                opacity=1,
                dash_array=[10, 100],
                curved=True,
                curve_factor= 200,
                show_arrow=False,
            ).add_child(text_label).add_to(map_obj)
        
          
        map_obj.save('main/templates/main/map.html')
        return render(request,'main/map.html')
    else:
        return render(request,'main/takeinput.html')