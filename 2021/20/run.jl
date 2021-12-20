

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




function readImage(lines)::Array{Int}
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
            



function readAlgorithm(algo::String)::String
    out = replace(replace(algo, '#' => '1'), '.' => '0')
    @assert length(algo) === length(out)
    out
end

@assert readAlgorithm("###..#..") === "11100100"


open("sample.txt", "r") do f
    lines = readlines(f)
    algorithm = readAlgorithm(popfirst!(lines))
    mat = readImage(lines[2:end])
    println(prettyPrint(mat))
    for _ in 1:2
        mat = doStep(algorithm, mat)
    end
    @assert sum(mat) === 35
end

open("input.txt", "r") do f
    lines = readlines(f)
    algorithm = readAlgorithm(popfirst!(lines))
    mat = readImage(lines[2:end])
    for _ in 1:2
        mat = doStep(algorithm, mat)
    end
    println(sum(mat))
end
