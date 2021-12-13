function parseNumbers(xy::String, delimiter::Char=',')
    (x, y) = split(xy, delimiter)
    [parse(Int, x), parse(Int, y)]
end

function isDot(line::String)::Bool
    match(r"[0-9]+,[0-9]+", line) !== nothing
end

function createDotMatrix(dots)
    dim = maximum(map(maximum, dots)) + 1
    dot_matrix = zeros(Int, (dim, dim))
    for (col, row) in dots
        # julia starts indexing at 1 :)
        col += 1
        row += 1
        dot_matrix[row, col] = 1
    end
    dot_matrix
end

function readInput(fname::String)
    open(fname, "r") do f
        lines = readlines(f)
        dots = filter(isDot, lines)
        # folds = filter(line -> ! isDot(line), lines)
        dots = map(parseNumbers, dots)
        return dots
    end
end

function part1(fname::String)
    dot_matrix = createDotMatrix(readInput(fname))
    println(dot_matrix)
end

part1("sample.txt")