function the_other_one(v, (a, b))
    if v == a
        return b
    elseif v == b
        return a
    end
end

@assert the_other_one("c", ["A", "c"]) == "A"
@assert the_other_one("A", ["A", "c"]) == "c"

function isSmallCave(vertex)::Bool
    match(r"^[A-Z]", String(vertex)) === nothing
end

isBigCave = x -> !isSmallCave(x)

@assert isBigCave("DX")
@assert isSmallCave("he")



function findNeighbors(vertex::String, path::Array{String}, edges)
    neighbors::Array{String} = []
    for edge in edges
        if vertex in edge
            neighbor = the_other_one(vertex, edge)
            if isSmallCave(neighbor) && (neighbor in path)
                # already visited, don't visit again
            else
                # big cave, or unvisited small cave
                neighbors = push!(neighbors, neighbor)
            end
        end
    end
    neighbors
end


function testFindNeighbors()
    path::Array{String} = []
    edges::Array{Array{String}} = [["A", "c"]]
    @assert findNeighbors("c", path, edges) == ["A", ]
end

function findPath(here::String, destination::String, path::Array{String}, edges)
    # depth-first search
    path = push!(path, here)
    if here == destination
        open("paths.txt", "a") do f
            map(s -> write(f, s * "-"), path)
            write(f, "\n")
        end
        return
    end
    for vertex in findNeighbors(here, path, edges)
        findPath(vertex, destination, path, edges)
    end
end




function part1(fname::String)
    open(fname, "r") do f
        edges = map(x -> map(String, split(x, "-")), readlines(f))
        empty_path::Array{String} = []
        # map(println, edges)
        if fname == "sample1.txt"
            @assert findNeighbors("start", empty_path, edges) == ["A", "b"]
            @assert findNeighbors("c", empty_path, edges) == ["A", ]
            @assert findNeighbors("end", empty_path, edges) == ["A", "b"]
            @assert findNeighbors("d", empty_path, edges) == ["b", ]

            path = ["start", "b"]
            # @assert findNeighbors("d", path, edges) == ["d","A", "end" ]
            println(findNeighbors("end", path, edges))

        end
        findPath("start", "end", empty_path, edges)
    end
end


part1("sample1.txt")