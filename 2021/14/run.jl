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

function isEven(i::Int)::Bool
    (i % 2) == 0
end

isOdd = x -> ! isEven(x)

@assert isEven(2)
@assert isOdd(1)


function combine_pairs(pairs::Array{String})::String
    reduce((p1, p2) -> p1 * p2[2:end], pairs)
end

@assert combine_pairs(["NCN", "NBC", "CHB"]) == "NCNBCHB"
@assert combine_pairs(["NCN", "NBC"]) == "NCNBC"



function doStep(template::String, rules::Dict)::String
    pairs = make_pairs(template)
    combine_pairs(map(pair -> insert(pair, rules), pairs))
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

function part1()
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
    end

    open("input.txt", "r") do f
        timing::Array{Int} = []
        (step, rules) = read_input(f)
        for i=1:40
            tick = datetime2unix(now())
            step = doStep(step, rules)
            tock = datetime2unix(now())
            elapsed = floor(tock - tick)  # seconds
            timing = push!(timing, elapsed)
            println(timing)
        end
        counts = countmap([c for c in step])
        println(counts)
        println(maximum(values(counts)) - minimum(values(counts)))
    end
end

part1()