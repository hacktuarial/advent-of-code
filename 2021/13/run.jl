using DelimitedFiles
function parseNumbers(xy::String, delimiter::Char=',')
    (x, y) = split(xy, delimiter)
    [parse(Int, x), parse(Int, y)]
end

function isDot(line::String)::Bool
    match(r"[0-9]+,[0-9]+", line) !== nothing
end

function readInput(fname::String)
    dots = readdlm("dots.txt", ',', Int)
    map(println, dots)
    open("folds.txt", "r") do f
        folds = map(line -> match(r"[xy]=[0-9]+", line).match, readlines(f))
        map(println, folds)
    end
end


parse("sample.txt")