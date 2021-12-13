function getNeighbors(row, col, lastRow, lastCol)
    neighbors = []
    steps = [-1, 0, 1]
    for row_step in steps
        for col_step in steps
            if row_step == 0 && col_step == 0
                continue
            end
            if 1 <= row + row_step <= lastRow
                # include diagonal
                neighbors = push!(neighbors, (row + row_step, col))
            end
            if 1 <= col + col_step <= lastCol
                neighbors = push!(neighbors, (row , col+ col_step))
            end
        end
    end
    neighbors
end

function read_input_string(in::String)::Array{Int}
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

function increment(energy::Int)
    if energy < 9
        return (energy + 1, false)
    elseif energy == 9
        # new flash
        return (10, true)
    else
        # already flashed
        return (10, false)
    end
end
    


function step(energy::Array{Int}, flashes::Int)
    new_energy = copy(energy)
    n_updates = ones(Int, size(energy))
    while maximum(n_updates) > 0
        for i=1:size(energy, 1)
            for j=1:size(energy, 2)
                if n_updates[i, j] == 0
                    continue
                end
                (new_value, flashed)=increment(new_energy[i, j])
                new_energy[i, j] = new_value
                n_updates[i, j] -= 1
                if flashed
                    flashes += 1
                    for (x, y) in getNeighbors(i, j, size(energy)...)
                        n_updates[x, y] += 1
                    end
                end
            end
        end
    end
    # change values for those that flashed back to 0
    for i=1:size(energy, 1)
        for j=1:size(energy, 2)
            new_energy[i, j] = new_energy[i, j] % 10
        end
    end
    (new_energy, flashes)
end

function part1(fname)
    open(fname, "r") do f
        arr = read_input_string(read(f, String))
        actual1 = step(arr, 0)
        expected_step1 = read_input_string("""6594254334
        3856965822
        6375667284
        7252447257
        7468496589
        5278635756
        3287952832
        7993992245
        5957959665
        6394862637""")
        if fname == "sample_input.txt"
            @assert actual1[1] == expected_step1
            actual2 = step(expected_step1, 0)
            expected_step2 = read_input_string("""8807476555
            5089087054
            8597889608
            8485769600
            8700908800
            6600088989
            6800005943
            0000007456
            9000000876
            8700006848""")
            println(actual2[1])
            @assert actual2[1] == expected_step2
            # count flashes
            flashes = 0
            for i in 1:10
                (arr, flashes) = step(arr, flashes)
            end
            @assert flashes == 204
        end

    end
end

part1("sample_input.txt")

# part1
open("input.txt", "r") do f
    # arr = read_input_string(read(f, String))
    arr = read_input_string("""4836484555
    4663841772
    3512484556
    1481547572
    7741183422
    8683222882
    4215244233
    1544712171
    5725855786
    1717382281""")
    # count flashes
    flashes = 0
    for i in 1:100
        (arr, flashes) = step(arr, flashes)
    end
    println(flashes)
end