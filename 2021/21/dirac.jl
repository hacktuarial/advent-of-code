# import Pkg; Pkg.add("DataStructures")
using DataStructures;
struct Player
    position::Int
    score::Int
end

function move(player::Player, rolls::Int)::Player
    new_position = (player.position + rolls)
    while new_position > 10
        new_position -= 10
    end
    new_score = player.score + new_position
    Player(new_position, new_score)
end

@assert move(Player(4, 0), 6) === Player(10, 10)

function rollThreeTimes(die::Int)
    first = die
    second = (first) % 100 + 1
    third = (second) % 100 + 1
    (first , second , third)
end

@assert rollThreeTimes(1) === (1, 2, 3)
@assert rollThreeTimes(99) === (99 , 100 , 1)
    


function step(p1::Player, die)
    rolls = rollThreeTimes(die)
    p1 = move(p1, sum(rolls))
    (p1, rolls[end] + 1)
end



function part1(p1::Int, p2::Int)
    die = 1
    p1 = Player(p1, 0)
    p2 = Player(p2, 0)
    rolls = 0
    while true
        p1, die = step(p1, die)
        rolls += 3
        if p1.score >= 1000
            break
        end
        p2, die = step(p2, die)
        rolls += 3
        if p2.score >= 1000
            break
        end
    end
    println(p1)
    println(p2)
    println(rolls)
    println(rolls * p1.score)
    println(rolls * p2.score)
end


part1(4, 8)
part1(4, 9)





import StatsBase: countmap
function tally()
    outcomes = []
    for i=1:3
        for j=1:3
            for k=1:3
                total = i + j + k
                outcomes = push!(outcomes, total)
            end
        end
    end
    println(countmap(outcomes))
end

tally()


struct GameStatus
    player1::Player
    player2::Player
    is_player1_turn::Bool
end


const final_score = 21
const rolls = Dict{Int, Int}(5 => 6, 4 => 3, 6 => 7, 7 => 6, 9 => 1, 8 => 3, 3 => 1)

function whoWon(game::GameStatus)::Int
    if game.player1.score >= final_score
        return 1
    elseif game.player2.score >= final_score
        return 2
    else
        return 0
    end
end


function makeNeighbor(game::GameStatus, moves::Int)::GameStatus
    if game.is_player1_turn
        newGame = GameStatus(move(game.player1, moves), game.player2, false)
    else
        newGame = GameStatus(game.player1, move(game.player2, moves), true)
    end
    newGame
end


function part2bfs(p1::Int, p2::Int)
    # this is all junk
    visited = Dict{GameStatus, Int}()
    queue = Queue{GameStatus}()
    initial = GameStatus(Player(p1, 0), Player(p2, 0), true)
    visited[initial] = 1
    enqueue!(queue, initial)
    wins = [0, 0]
    while length(queue) > 0 & minimum(wins) < 444356092776315
        game = dequeue!(queue)
        winner = whoWon(game)
        if winner > 0
            wins[winner] += visited[game]
            continue
        end
        for roll in keys(rolls)
            n = rolls[roll]
            neighbor = makeNeighbor(game, roll)
            if haskey(visited, neighbor)
                # it's already somewhere in the queue, just increase 
                # how many times it's been visited
                visited[neighbor] += n
            else
                visited[neighbor] = n
                enqueue!(queue, neighbor)
            end
        end
    end
    println(sum(values(visited)))
    wins
end

struct Wins
    wins1::Int
    wins2::Int
end

function repeat(wins::Wins, n::Int)
    Wins(n * wins.wins1, n * wins.wins2)
end

function add(left::Wins, right::Wins)::Wins
    Wins(left.wins1 + right.wins1, left.wins2 + right.wins2)
end

function part2recursive(game::GameStatus)::Wins
    # structure based on https://github.com/ClouddJR/AdventOfCode2021/blob/master/src/main/kotlin/com/clouddjr/advent2021/Day21.kt
    if game.player1.score >= final_score
        return Wins(1, 0)
    elseif game.player2.score >= final_score
        return Wins(0, 1)
    end
    wins = Wins(0, 0)
    for (roll, n) in rolls
        wins = add(wins, repeat(part2recursive(makeNeighbor(game, roll)), n))
    end
    wins
end



initial = GameStatus(Player(4, 0), Player(9, 0), true)
println(part2recursive(initial))