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
    empty_path::Array{String} = []
    edges::Array{Array{String}} = [["start", "A"], ["start", "b"], ["A", "c"], ["A", "b"], ["b", "d"], ["A", "end"], ["b", "end"]]
    @assert findNeighbors("c", empty_path, edges) == ["A", ]
    @assert findNeighbors("start", empty_path, edges) == ["A", "b"]
    @assert findNeighbors("c", empty_path, edges) == ["A", ]
    @assert findNeighbors("end", empty_path, edges) == ["A", "b"]
    @assert findNeighbors("d", empty_path, edges) == ["b", ]
    path = ["start"]
    @assert ! ("start" in findNeighbors("A", path, edges))
    @assert "end" in findNeighbors("A", path, edges)
end

testFindNeighbors()

function findPath(here::String, destination::String, path::Array{String}, edges)
    # depth-first search
    if here == destination
        open("paths.txt", "a") do f
            map(s -> write(f, s * "-"), path)
            write(f, "\n")
        end
        return
    end
    path = push!(path, here)
    for vertex in findNeighbors(here, path, edges)
        findPath(vertex, destination, copy(path), edges)
    end
end




function part1(fname::String)
    open(fname, "r") do f
        edges = map(x -> map(String, split(x, "-")), readlines(f))
        empty_path::Array{String} = []
        # map(println, edges)
        if fname == "sample1.txt"

        end
        findPath("start", "end", empty_path, edges)
    end
end


part1("input.txt")