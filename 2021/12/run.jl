function findVertices(edges)
    vertices = Set()
    for (v1, v2) in edges
        vertices += v1
        vertices += v2
    end
    vertices
end

function the_other_one(v, (a, b))
    if v == a
        return b
    elseif v == b
        return a
    end
end

function isSmallCave(vertex)::Bool
    match(r"^[A-Z]", String(vertex)) === nothing
end

isBigCave = x -> !isSmallCave(x)

@assert isBigCave("DX")
@assert isSmallCave("he")



function findNeighbors(vertex, path, edges)
    neighbors = []
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

function findPath(here::String, destination::String, path::Array{String}, edges)
    # depth-first search
    path = push!(path, here)
    if here === destination
        open("paths.txt", "a") do f
            map(s -> write(f, s * "-"), path)
            write(f, "\n")
        end
    end
    for vertex in findNeighbors(here, path, edges)
        findPath(vertex, destination, path, edges)
    end
    # backtrack
    # pop!(path)
end




function part1(fname::String)
    open(fname, "r") do f
        edges = map(x -> split(x, "-"), readlines(f))
        edges = map(x -> map(String, x), edges)
        path::Array{String} = []
        findPath("start", "end", path, edges)
    end
end


part1("sample2.txt")