using Dates
using StatsBase

function insert(pair::String, rules::Dict)::String
    if haskey(rules, pair)
        out = pair[1] * rules[pair] * pair[2]
    else
        out = pair
    end
    out
end
@assert insert("CH", Dict("CH"=>'B')) === "CBH"
@assert insert("CH", Dict("AH"=>'B')) === "CH"

function make_pairs(template::String)::Array{String}
    [template[i:i+1] for i in 1:(length(template)-1)]
end

@assert make_pairs("ABC") == ["AB", "BC"]

function combine_pairs(pairs::Array{String})::String
    reduce((p1, p2) -> p1 * p2[2:end], pairs)
end

@assert combine_pairs(["NCN", "NBC", "CHB"]) == "NCNBCHB"
@assert combine_pairs(["NCN", "NBC"]) == "NCNBC"


function updateCounts(string::String, counts::Dict)
    for c::Char in string[2:end]
        if haskey(counts, c)
            counts[c] += 1
        else
            counts[c] = 1
        end
    end
end


function explode(template::String, rules::Dict, steps::Int, counts::Dict)
    lk = ReentrantLock()
    if steps === 0
        # update counts
        # https://docs.julialang.org/en/v1/manual/multi-threading/#man-multithreading
        begin
            lock(lk)
            try
                updateCounts(template, counts)
            finally
                unlock(lk)
            end
        end
        return nothing
    end
    pairs = make_pairs(template)
    for pair in pairs
        explode(insert(pair, rules), rules, steps-1, counts)
    end
end



function doStep(template::String, rules::Dict)::String
    pairs = make_pairs(template)
    combine_pairs(map(pair -> insert(pair, rules), pairs))
end


function minMaxCounts(template::String)::Int
    counts = countmap([c for c in template])
    minMaxCounts(counts)
end

function minMaxCounts(counts::Dict)::Int
    maximum(values(counts)) - minimum(values(counts))
end


function read_input(f)
    lines = readlines(f)
    template = String(strip(lines[1]))
    rules = Dict{String, String}()
    for line in lines[3:end]
        (left, right) = split(line, "->")
        rules[strip(left)] = strip(right)
    end
    (template, rules)
end

open("sample.txt", "r") do f
    (template, rules) = read_input(f)
    step1 = doStep(template, rules)
    @assert step1 == "NCNBCHB"
    step2 = doStep(step1, rules)
    @assert step2 == "NBCCNBBBCBHCB"
    step3 = doStep(step2, rules)
    @assert step3 == "NBBBCNCCNBBNBNBBCHBHHBCHB"
    step4 = doStep(step3, rules)
    @assert step4 == "NBBNBNBBCCNBCNCCNBBNBBNBBBNBBNBBCBHCBHHNHCBBCBHCB"
    for _ in 1:10
        template = doStep(template, rules)
    end

    # the scalable way
    # need to seed this with the first character of the template
    counts::Dict{Char, Int} = Dict('N' => 1)
    explode("NNCB", rules, 10, counts)
    @assert minMaxCounts(counts) === 1588
end

open("input.txt", "r") do f
    (template, rules) = read_input(f)
    counts::Dict{Char, Int} = Dict(template[1]::Char => 1)
    # explode(template, rules, 20, counts)
    # println(minMaxCounts(counts))
end