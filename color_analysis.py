import os

def read_stats_file(file_name):
    stats = {}
    file = open(file_name, "r")
    for line in file:
        segments = line.strip().split(";")
        
        color_list = segments[1].split(",")
        color_combination_key = ""
        for color in ["W", "U", "B", "R", "G"]:
            if color in color_list:
                color_combination_key += color
                
        meta_percentage = float(segments[2])

        if color_combination_key not in stats:
            stats[color_combination_key] = meta_percentage
        else:
            stats[color_combination_key] += meta_percentage
        
    file.close()
    return stats


def normalize_representation(representation):
    total = 0
    for value in representation.values():
        total += value
        
    new_representation = {}
    for key, value in representation.items():
        new_representation[key] = value/total
    return new_representation


formats = ["standard", "modern", "pioneer", "pauper"]

color_names = {"W" : "White", "U" : "Blue", "B" : "Black", "R" : "Red", "G" : "Green"}

color_combination_names = {
    "" : "Colorless",
    "W" : "Mono White",
    "U" : "Mono Blue",
    "B" : "Mono Black",
    "R" : "Mono Red",
    "G" : "Mono Green",
    "WU" : "Azorius",
    "WB" : "Orzhov",
    "WR" : "Boros",
    "WG" : "Selesnya",
    "UB" : "Dimir",
    "UR" : "Izzet",
    "UG" : "Simic",
    "BR" : "Rakdos",
    "BG" : "Golgari",
    "RG" : "Gruul",
    "WUB" : "Esper",
    "WUR" : "Jeskai",
    "WUG" : "Bant",
    "WBR" : "Mardu",
    "WBG" : "Abzan",
    "WRG" : "Naya",
    "UBR" : "Grixis",
    "UBG" : "Sultai",
    "URG" : "Temur",
    "BRG" : "Jund",
    "WUBR" : "Yore",
    "WUBG" : "Witch",
    "WURG" : "Ink",
    "WBRG" : "Dune",
    "UBRG" : "Glint",
    "WUBRG" : "Five Color"
}

all_stats = {}

# Reading all data

for format_name in formats:
    all_stats[format_name] = {}

    for file_name in os.listdir(format_name):
        date_segments = [int(x) for x in file_name.split(".")[0].split("_")]
        date_segments.reverse()
        date_segments = tuple(date_segments)
        date_key = date_segments

        stats = read_stats_file(format_name + "/" + file_name)
        all_stats[format_name][date_key] = stats


all_mono_colored_representation = {}
all_color_combination_representation = {}

for format_name in formats:
    format_mono_colored_representation = {}
    format_color_combination_representation = {}
    
    for date_key, stats in all_stats[format_name].items():
        for color_combination, meta_percentage in stats.items():
            if color_combination not in format_color_combination_representation:
                format_color_combination_representation[color_combination] = meta_percentage
            else:
                format_color_combination_representation[color_combination] += meta_percentage
                
            for color in ["W", "U", "B", "R", "G"]:
                if color in color_combination:
                    if color not in format_mono_colored_representation:
                        format_mono_colored_representation[color] = meta_percentage
                    else:
                        format_mono_colored_representation[color] += meta_percentage

    format_mono_colored_representation = normalize_representation(format_mono_colored_representation)
    format_color_combination_representation = normalize_representation(format_color_combination_representation)

    color_combination_list = []
    for color_combination, meta_percentage in format_color_combination_representation.items():
        color_combination_list.append((color_combination, meta_percentage))
    color_combination_list = sorted(color_combination_list, key = lambda item: item[1])
    color_combination_list.reverse()

    print("Stats for {}".format(format_name))
    print("=" * 40)
    print("Single color representation:")
    for color in ["W", "U", "B", "R", "G"]:
        print("{}:\t{:.3f}%".format(color_names[color], format_mono_colored_representation[color] * 100))
    print("=" * 40)
    print("Color combination representation:")
    for color_combination, meta_percentage in color_combination_list:
        print("{}:\t{:.3f}%\t({})".format(color_combination, meta_percentage * 100, color_combination_names[color_combination]))
    print("=" * 40)
    print("\n")

    for color, meta_percentage in format_mono_colored_representation.items():
        if color not in all_mono_colored_representation:
            all_mono_colored_representation[color] = meta_percentage
        else:
            all_mono_colored_representation[color] += meta_percentage

    for color_combination, meta_percentage in format_color_combination_representation.items():
        if color_combination not in all_color_combination_representation:
            all_color_combination_representation[color_combination] = meta_percentage
        else:
            all_color_combination_representation[color_combination] += meta_percentage

all_mono_colored_representation = normalize_representation(all_mono_colored_representation)
all_color_combination_representation = normalize_representation(all_color_combination_representation)

color_combination_list = []
for color_combination, meta_percentage in all_color_combination_representation.items():
    color_combination_list.append((color_combination, meta_percentage))
color_combination_list = sorted(color_combination_list, key = lambda item: item[1])
color_combination_list.reverse()

print("Stats for all formats")
print("=" * 40)
print("Single color representation:")
for color in ["W", "U", "B", "R", "G"]:
    print("{}:\t{:.3f}%".format(color_names[color], all_mono_colored_representation[color] * 100))
print("=" * 40)
print("Color combination representation:")
for color_combination, meta_percentage in color_combination_list:
    print("{}:\t{:.3f}%\t({})".format(color_combination, meta_percentage * 100, color_combination_names[color_combination]))
print("=" * 40)
