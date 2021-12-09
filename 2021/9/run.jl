

function getNeighbors(row, col, lastRow, lastCol)
    neighbors = []
    steps = [-1, 1]
    for step in steps
        if 1 <= row + step <= lastRow
            neighbors = push!(neighbors, (row + step, col))
        end
        if 1 <= col + step <= lastCol
            neighbors = push!(neighbors, (row, col + step))
        end
    end
    neighbors
end

function isLowPoint(mat::Array, i::Int, j::Int):: Bool
    neighbors = getNeighbors(i, j, size(mat, 1), size(mat, 2))
    lowPoint = true
    for neighbor in neighbors
        lowPoint = lowPoint && (mat[i, j] < mat[neighbor[1], neighbor[2]])
    end
    lowPoint
end

function read_input_string(in::String)
    rows = filter(row -> length(row) > 0, split(in, "\n"))
    n_cols = length(rows[1])
    n_rows = length(rows)
    mat = zeros(Int, (n_rows, n_cols))
    for (i, row) in enumerate(rows)
        for (j, v) in enumerate(row)
            mat[i, j] =  parse(Int, v)
        end
    end
    mat
end

function findLowPoints(mat::Matrix{Int})
    points = []
    # can probably use a generator expression here
    for row=1:size(mat, 1)
        for col=1:size(mat, 2)
            if isLowPoint(mat, row, col)
                points = push!(points, (row, col))
            end
        end
    end
    points
end

function computeRiskLevel(mat::Matrix{Int}, points)
    riskLevel = 0
    for point in points
        riskLevel += 1 + mat[point...]
    end
    return riskLevel
end


function basinSize(mat::Matrix{Int}, startRow::Int, startCol::Int)
    """Breadth-first search from this starting point"""
    basinSize = 1
    visited = zeros(Int8, size(mat))
    visited[startRow, startCol] = 1
    queue = [(startRow, startCol)]
    while length(queue) > 0
        v = popfirst!(queue)
        for neighbor in getNeighbors(v[1], v[2], size(mat, 1), size(mat, 2))
            if visited[neighbor...] == 0
                visited[neighbor...] = 1
                if mat[neighbor...] < 9
                    basinSize += 1
                    queue = push!(queue, neighbor)
                end
            end
        end
    end
    basinSize
end


function part2(mat)
    lowPoints = findLowPoints(mat)
    # splat point per https://docs.julialang.org/en/v1/manual/functions/
    basins = map(point -> basinSize(mat, point...), lowPoints)
    basins = sort(basins)
    # https://julia.school/julia/arrays/#how-to-get-the-last-n-items-in-an-array-in-julia
    reduce((x, y) -> x * y, last(basins, 3))
end


open("sample_input.txt", "r") do f
    mat = read_input_string(read(f, String))
    @assert computeRiskLevel(mat, findLowPoints(mat)) == 15
    @assert basinSize(mat, 1, 1) == 3
    @assert basinSize(mat, 1, 10) == 9
    @assert part2(mat) == 1134
end
    



open("input.txt", "r") do f
    mat = read_input_string(read(f, String))
    @assert 548 == computeRiskLevel(mat, findLowPoints(mat))
    println(part2(mat))
end