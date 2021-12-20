

function binary2int(binary::String)::Int
    parse(Int, binary; base=2)
end

@assert binary2int("000100010") === 34


function safeGet(mat::Array{Int}, row::Int, col::Int)::Char
    try
        return mat[row, col]
    catch BoundsError
        return '0'
    end
end

function enhance(mat::Array{Int}, row::Int, col::Int, algorithm::String)::Char
    pixels = ""
    for new_row=(row-1):row+1
        for new_col=(col-1):(col+1)
            pixels = pixels * safeGet(mat, new_row, new_col)
        end
    end
    algorithm_index = 1 + binary2int(pixels)
    println((pixels, algorithm_index, algorithm[algorithm_index]))
    algorithm[algorithm_index]
end


function part1(algorithm::String, image::Array{Int})::Array{Int}
    # initialize empty matrix
    new_image = zeros(Int, size(image))
    for i=1:size(new_image, 1)
        for j=1:size(new_image, 2)
            new_image[i, j] = enhance(image, i, j, algorithm)
        end
    end
    new_image
end


function translate(s::String)::String
    s = replace(s, '.' => '0')
    replace(s, '#' => 1)
end


function readImage(s::String)::Array{Int}
    img = translate(s)
    lines = split(img, "\n")
    out = zeros((length(lines), length(lines[1])))
    for (row, line) in enumerate(lines)
        for (col, c) in enumerate(line)
            out[row, col] = c
        end
    end
    out
end




algorithm="..#.#..#####.#.#.#.###.##.....###.##.#..###.####..#####..#....#..#..##..###..######.###...####..#..#####..##..#.#####...##.#.#..#.##..#.#......#.###.######.###.####...#.##.##..#..#..#####.....#.#....###..#.##......#.....#..#..#..##..#...##.######.####.####.#.#...#.......#..#.#.#...####.##.#......#..#...##.#.##..#...##.#.##..###.#......#.#.......#.#.#.####.###.##...#.....####.#..#..#.##.#....##..#.####....##...##..#...#......#.#.......#.......##..####..#...#.#.#...##..#.#..###..#####........#..####......#..#"
algorithm = translate(algorithm)
img = """#..#.
#....
##..#
..#..
..###"""
println(part1(algorithm, readImage(img)))