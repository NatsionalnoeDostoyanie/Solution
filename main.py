from city_grid import CityGrid


def main():
    city = CityGrid(7, 7)

    custom_grid = [
        [0, 0, 2, 2, 2, 2, 0],
        [0, 2, 0, 0, 0, 0, 2],
        [0, 0, 2, 0, 0, 0, 2],
        [0, 0, 2, 0, 0, 0, 2],
        [0, 0, 2, 0, 0, 0, 2],
        [0, 0, 0, 2, 0, 0, 2],
        [0, 0, 0, 0, 2, 2, 0],
    ]
    city.set_custom_grid(custom_grid)

    print(city)
    city.visualize_grid()

    '''
    city.place_minimal_towers()

    print(city)
    city.visualize_grid()
    '''
    if input('Do you want to build most reliable path (there must be at least three connected towers on the grid) (y/n)?\n') == 'y':
        start_tower_str = input('Enter the start tower coordinates (сounting coordinates from zero, top left) (x, y): ')
        end_tower_str = input('Enter the end tower coordinates (сounting coordinates from zero, top left) (x, y): ')

        start_tower = tuple(map(int, start_tower_str.split(',')))
        end_tower = tuple(map(int, end_tower_str.split(',')))

        city.visualize_grid(start_tower, end_tower)


if __name__ == '__main__':
    main()
