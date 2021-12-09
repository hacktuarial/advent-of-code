

function isLowPoint(mat::Array, i::Int, j::Int):: Bool
    lessThanLeft = (j == 1) || (mat[i, j-1] > mat[i, j])
    lessThanRight = (j == size(mat, 2)) || (mat[i, j+1] > mat[i, j])
    lessThanAbove = (i==1) || (mat[i-1, j] > mat[i, j])
    lessThanBelow = (i==size(mat, 1)) || (mat[i+1, j] > mat[i, j])
    lessThanLeft && lessThanRight && lessThanAbove && lessThanBelow
end

@assert 1 == 1

function read_input_string(in::String)
    rows = split(in, "\n")
    n_cols = length(rows[1])
    n_rows = length(rows)
    # mat = Matrix{Int}(n_rows, n_cols)
    # mat = Array{Int}(n_rows, n_cols)
    mat = zeros(Int, (n_rows, n_cols))
    for (i, row) in enumerate(rows)
        for (j, v) in enumerate(row)
            mat[i, j] =  parse(Int, v)
        end
    end
    # println(size(mat))
    mat
end

function findLowPoints(mat::Matrix{Int})
    riskLevel::Int = 0
    for row=1:size(mat, 1)
        for col=1:size(mat, 2)
            if isLowPoint(mat, row, col)
                # println((row, col))
                riskLevel += 1 + mat[row, col]
            end
        end
    end
    return riskLevel
end


input_string =
"""
2199943210
3987894921
9856789892
8767896789
9899965678"""

@assert findLowPoints(read_input_string(input_string)) == 15


