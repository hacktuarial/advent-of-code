
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
    (algorithm[algorithm_index] === '#') ? 1 : 0
end

function pad(mat::Array{Int}, pad::Int; withZero=true)::Array{Int}
    """ add 'pad' zeros on every side.
    size -> (size + 2 * pad, size + 2*pad)

    if input matrix is 5x5 and pad=2
        output will be 9x9
        rows 1,2 are all 0
        rows 3-7 are the original matrix
        rows 8-9 are all 0
        likewise for columns
        end = 9
    """
    if withZero
        new_mat = zeros(Int, (size(mat, 1) + 2*pad, size(mat, 2) + 2*pad))
    else
        new_mat = ones(Int, (size(mat, 1) + 2*pad, size(mat, 2) + 2*pad))
    end
    new_mat[(1+pad):(end-pad), (1+pad):(end-pad)] = copy(mat)
    new_mat
end

function testPad()
    mat = [1 2 3; 4 5 6; 7 8 9;]
    actual = pad(mat, 2)
    expected = [
                0 0 0 0 0 0 0;
                0 0 0 0 0 0 0;
                0 0 1 2 3 0 0;
                0 0 4 5 6 0 0;
                0 0 7 8 9 0 0;
                0 0 0 0 0 0 0;
                0 0 0 0 0 0 0;
    ]
    @assert actual == expected
end

testPad()

function doStep(algorithm::String, image::Array{Int})::Array{Int}
    # initialize empty matrix
    new_image = zeros(size(image))
    for i=1:size(new_image, 1)
        for j=1:size(new_image, 2)
            new_image[i, j] =  enhance(image, i, j, algorithm)
        end
    end
    new_image[2:end-1, 2:end-1]
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

            

open("sample.txt", "r") do f
    lines = readlines(f)
    algorithm = popfirst!(lines)
    mat = readImage(lines[2:end])
    # println(prettyPrint(mat))
    mat = pad(mat, 10)
    for _ in 1:2
        mat = doStep(algorithm, mat)
        mat = pad(mat, 2, withZero=mat[1, 1]==0)
    end
    @assert sum(mat) === 35
end

open("input.txt", "r") do f
    lines = readlines(f)
    algorithm = popfirst!(lines)
    mat = readImage(lines[2:end])
    @assert size(mat) === (100, 100)
    mat = pad(mat, 11)
    @assert minimum(mat) === 0
    @assert maximum(mat) === 1
    for _ in 1:50
        println(size(mat))
        mat = doStep(algorithm, mat)
        mat = pad(mat, 2, withZero=mat[1, 1]==0)
    end
    println(sum(mat))
end
