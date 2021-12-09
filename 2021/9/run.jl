

function isLowPoint(mat::Array, i::Int, j::Int):: Bool
    lessThanLeft = (j == 1) || (mat[i, j-1] > mat[i, j])
    lessThanRight = (j == size(mat, 2)) || (mat[i, j+1] > mat[i, j])
    lessThanAbove = (i==1) || (mat[i-1, j] > mat[i, j])
    lessThanBelow = (i==size(mat, 1)) || (mat[i+1, j] > mat[i, j])
    lessThanLeft && lessThanRight && lessThanAbove && lessThanBelow
end

@assert 1 == 1

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
        riskLevel += 1 + mat[point[1], point[2]]
    end
    return riskLevel
end



open("sample_input.txt", "r") do f
    mat = read_input_string(read(f, String))
    @assert computeRiskLevel(mat, findLowPoints(mat)) == 15
end
    



open("input.txt", "r") do f
    mat = read_input_string(read(f, String))
    println(computeRiskLevel(mat, findLowPoints(mat)))
end