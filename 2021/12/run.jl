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


function nVisits(vertex::String, path)::Int
    # how many times has this path been through a particular cave
    length(filter(v -> v == vertex, path))
end

function doubleVisit(path, maxVisits::Int)::Bool
    small_caves = filter(isSmallCave, path)
    visits = map(cave -> nVisits(cave, path), small_caves)
    (length(visits) == 0) ? false : maximum(visits) == maxVisits
end

function canVisit(vertex::String, path)::Bool
    if vertex == "start"
        # can only visit start
        return false
    elseif vertex == "end"
        return true
    elseif isBigCave(vertex)
        return true
    else
        # small cave
        # if any small cave has been visited twice, this one can only be visited once
        if doubleVisit(path, 1)
            return !(vertex in path)
        else
            return true
        end
    end
end


function findNeighbors(vertex::String, path::Array{String}, edges)
    neighbors::Array{String} = []
    for edge in edges
        if vertex in edge
            neighbor = the_other_one(vertex, edge)
            if canVisit(neighbor, path)
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

function findPath(here::String, destination::String, path::Array{String}, edges, paths)
    # depth-first search
    if here == destination
        paths = push!(paths, path)
        return
    end
    path = push!(path, here)
    for vertex in findNeighbors(here, path, edges)
        findPath(vertex, destination, copy(path), edges, paths)
    end
end




function part1(fname::String)
    open(fname, "r") do f
        edges = map(x -> map(String, split(x, "-")), readlines(f))
        empty_path::Array{String} = []
        paths = []
        # map(println, edges)
        findPath("start", "end", empty_path, edges, paths)
        println(length(paths))
    end
end


part1("input.txt")