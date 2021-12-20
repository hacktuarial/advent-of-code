

function binary2int(binary::String)::Int
    parse(Int, binary; base=2)
end

@assert binary2int("000100010") === 34


function safeGet(mat::Array{Int}, row::Int, col::Int)::Int
    try
        return mat[row, col]
    catch BoundsError
        return 0
    end
end

function enhance(mat::Array{Int}, row::Int, col::Int, algorithm::String)::Int
    pixels = ""
    for new_row=(row-1):row+1
        for new_col=(col-1):(col+1)
            pixels = pixels * string(safeGet(mat, new_row, new_col))
        end
    end
    algorithm_index = 1 + binary2int(pixels)
    # println((pixels, algorithm_index, algorithm[algorithm_index]))
    (algorithm[algorithm_index] === '1') ? 1 : 0
end

function pad(mat::Array{Int}, pad::Int)::Array{Int}
    """ add 'pad' zeros on every side.
    size -> (size + 2 * pad, size + 2*pad)
    """
    new_mat = zeros(size(mat, 1) + 2*pad, size(mat, 2) + 2*pad)
    new_mat[1+pad:end-pad, 1+pad:end-pad] = copy(mat)
    new_mat
end

function doStep(algorithm::String, image::Array{Int})::Array{Int}
    # initialize empty matrix
    padded_image = pad(image, 3)
    new_image = zeros(Int, size(padded_image))
    for i=1:size(new_image, 1)
        for j=1:size(new_image, 2)
            val = enhance(padded_image, i, j, algorithm)
            @assert val <= 1
            new_image[i, j] =  val
        end
    end
    new_image
end




function readImage(s::String)::Array{Int}
    lines = split(s, "\n")
    out = zeros((length(lines), length(lines[1])))
    for (row, line) in enumerate(lines)
        for (col, c) in enumerate(line)
            out[row, col] = (c === '#') ? 1 : 0
        end
    end
    out
end


function prettyPrint(img::Array{Int})::String
    out = ""
    for row=1:size(img, 1)
        for col=1:size(img, 2)
            out = out * ((img[row, col] === 1) ? '#' : '.')
        end
        out *= "\n"
    end
    out
end
            


algorithm="00101001111101010101110110000011101101001110111100111110010000100100110011100111111011100011110010011111001100101111100011010100101100101000000101110111111011101111000101101100100100111110000010100001110010110000001000001001001001100100011011111101111011110101000100000001001010100011110110100000010010001101011001000110101100111010000001010000000101010111101110110001000001111010010010110100001100101111000011000110010001000000101000000010000000110011110010001010100011001010011100111110000000010011110000001001"
img = """#..#.
#....
##..#
..#..
..###"""
println(prettyPrint(readImage(img)))
# println(prettyPrint(pad(readImage(img), 1)))
# println(prettyPrint(pad(readImage(img), 2)))
output = doStep(algorithm, readImage(img))
output = doStep(algorithm, output)
@assert sum(output) === 35


function readAlgorithm(algo::String)::String
    replace(replace(algo, '#' => '1'), '.' => '0')
end

@assert readAlgorithm("###..#..") === "11100100"

open("input.txt", "r") do f
    lines = readlines(f)
    algorithm = readAlgorithm(popfirst!(lines))
    mat = join(lines[3:end], "\n")
    mat = readImage(mat)
    for _ in 1:2
        mat = doStep(algorithm, mat)
    end
    println(sum(mat))
end
