function getNeighbors(row, col, lastRow, lastCol)
    neighbors = []
    steps = [-1, 0, 1]
    for row_step in steps
        for col_step in steps
            if row_step == 0 && col_step == 0
                continue
            end
            neighbors = push!(neighbors, (row + row_step, col + col_step))
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


function step(energy::Array{Int})
    new_energy = 1 .+ energy  # broadcast
    flashed = zeros(size(energy))
    all_done = false
    while ! all_done
        prior_flashes = sum(flashed)
        for i=1:size(energy, 1)
            for j=1:size(energy, 2)
                if new_energy[i, j] >= 10 && flashed[i, j] == 0
                    flashed[i, j] = 1
                    for (x, y) in getNeighbors(i, j, size(energy)...)
                        try
                            new_energy[x, y] += 1
                        catch BoundsError
                            # do nothing
                        end
                    end
                end
            end
        end
        all_done = sum(flashed) == sum(prior_flashes)
    end
    for i=1:size(energy, 1)
        for j=1:size(energy, 2)
            if new_energy[i, j] >= 10
                new_energy[i, j] = 0
            end
        end
    end
    (new_energy,  sum(flashed))
end 

function part1(fname)
    open(fname, "r") do f
        arr = read_input_string(read(f, String))
        actual1 = step(arr)
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
            actual2 = step(expected_step1)
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
            total_flashes = 0
            for i in 1:10
                (arr, flashes) = step(arr)
                total_flashes += flashes
            end
            @assert total_flashes == 204
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
    iter = 0
    while true
        iter += 1
        (arr, flashes) = step(arr)
        if flashes == size(arr, 1) * size(arr, 2)
            println(iter)
            break
        end
    end
end