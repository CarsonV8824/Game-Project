import os
import sys
import json
import networkx as nx

# Add project root to path so maps module can be found
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from maps.tiles import map_colors, collision_tiles

def convert_map_to_coords_dict(map_dict: list) -> dict:
    coords = {}
    for r, row in enumerate(map_dict):
        for c, cell in enumerate(row):
            coords[(r, c)] = cell
    return coords

def load_maps(selected_map_name="grasslands") -> list:
    maps_file_path = os.path.join("maps", "maps.json")
    with open(maps_file_path, "r") as f:
        maps_data = json.load(f)
    return maps_data[selected_map_name]["map"]

def grid_to_graph() -> nx.Graph:
    blocked = collision_tiles()
    grid=load_maps()
    rows = len(grid)
    cols = len(grid[0])

    G = nx.Graph()

    # Directions: up, down, left, right
    directions = [(0,1), (0,-1), (1,0), (-1,0)]

    for r in range(rows):
        for c in range(cols):

            # Skip blocked tiles
            if grid[r][c] in blocked:
                continue

            # Add node for this tile
            G.add_node((r, c))

            # Add edges to neighbors
            for dr, dc in directions:
                nr, nc = r + dr, c + dc

                if 0 <= nr < rows and 0 <= nc < cols:
                    if grid[nr][nc] not in blocked:
                        G.add_edge((r, c), (nr, nc))

    return G 

def shortest_path_networkx(gameMap=None, mapName="grasslands", start_pos=None):
    """Get shortest path to objective. If start_pos is provided, return path from that specific spawn point."""
    if gameMap is not None:
        map_dict = gameMap
    else:
        map_dict = load_maps(mapName)
    start = [(r, c) for r, row in enumerate(map_dict) for c, cell in enumerate(row) if cell == "enemy_spawn"]
    goal_coords = [(r, c) for r, row in enumerate(map_dict) for c, cell in enumerate(row) if cell == "objective"]
    
    # Find walkable tiles adjacent to the objective
    blocked = collision_tiles()
    adjacent_walkable = []
    if goal_coords:
        goal_r, goal_c = goal_coords[0]
        directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]
        for dr, dc in directions:
            nr, nc = goal_r + dr, goal_c + dc
            if 0 <= nr < len(map_dict) and 0 <= nc < len(map_dict[0]):
                if map_dict[nr][nc] not in blocked:
                    adjacent_walkable.append((nr, nc))
    
    if not adjacent_walkable or not start:
        return []
    
    G = grid_to_graph()
    
    # If a specific start position is provided, return path from that position
    if start_pos and start_pos in start:
        try:
            path = nx.shortest_path(G, source=start_pos, target=adjacent_walkable[0])
            # Append the objective as the final destination
            if goal_coords:
                path.append(goal_coords[0])
            return path
        except Exception as e:
            print(f"Error finding shortest path: {e}")
            return []
    
    # Otherwise return paths from all spawn points
    final = []
    for pos in start:
        try:
            path = nx.shortest_path(G, source=pos, target=adjacent_walkable[0])
            # Append the objective as the final destination
            if goal_coords:
                path.append(goal_coords[0])
            final.append(path)
        except Exception as e:
            print(f"Error finding shortest path: {e}")
    return final

if __name__ == "__main__":
    try:
        path = shortest_path_networkx()
        print(f"Shortest path from (0, 0) to (4, 6): {path}")
    except Exception as e:
        print(f"Error: {e}")