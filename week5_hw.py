import sys

def read_input(filename):
    with open(filename) as f:
        cities = []
        for line in f.readlines()[1:]:  # Ignore the first line.
            xy = line.split(',')
            cities.append((float(xy[0]), float(xy[1])))
        return cities


#2点間の距離を返す
def distance(a, b):
    dx = (a[0]-b[0])**2
    dy = (a[1]-b[1])**2
    return (dx + dy)**0.5


#巡回路の総距離を返す
def route_length(cities, route):
    sum = 0
    for i in range(len(route)):
        a = cities[route[i]]
        b = cities[route[(i+1)%len(route)]]
        sum += distance(a, b)
    return sum


#貪欲法
def greedy_algorithm(cities):
    visited = [False] * len(cities)
    current = 0
    visited[0] = True
    route = [0]

    for _ in range(len(cities)-1):
        min_dist = float('inf')
        min_point = None
        for i in range(len(cities)):
            if not visited[i]:
                dist = distance(cities[i], cities[current])
                if dist < min_dist:
                    min_dist = dist
                    min_point = i
        route.append(min_point)
        visited[min_point] = True
        current = min_point
    
    return route


#2-opt
def two_opt(cities, route):
    route_len = len(route)

    improved = True #更新の有無

    while improved:
        improved = False

        for i in range(route_len-1):
            for j in range(i+2, route_len):

                #先頭と2番目の組と、末尾と先頭の組は、先頭が被るので交換不可
                if i == 0 and j == route_len-1:
                    continue

                a, b = cities[route[i]], cities[route[i+1]]
                c, d = cities[route[j]], cities[route[(j+1)%route_len]]

                delta = distance(a, c) + distance(b, d) - distance(a, b) - distance(c, d)

                if delta < 0:
                    #aまでのリスト + b~cを逆順にしたリスト + d以降のリスト
                    route = route[:i+1] + route[i+1:j+1][::-1] + route[j+1:]
                    improved = True
    return route


def main():
    if len(sys.argv) != 3:
        print("Usage: python3 week5_hw.py input_csv, output_csv")
        return

    input_file = sys.argv[1]
    output_file = sys.argv[2]
    cities = read_input(input_file)
    route = greedy_algorithm(cities)
    new_route = two_opt(cities, route)
    output_str = 'index\n'+'\n'.join(map(str,new_route))
    with open(output_file, 'w') as f:
        f.write(output_str)

if __name__ == "__main__":
    main()
