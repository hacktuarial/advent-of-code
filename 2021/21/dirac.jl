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
    finished::Bool
    is_player1_turn::Bool
end


function update(outcomes::Dict{GameStatus, Int}, previousGame::GameStatus, newGame::GameStatus, n::Int)
    # update in place
    try
        n += outcomes[previousGame]
    catch KeyError
        # do nothing
    end

    try
        outcomes[newGame] += n
    catch KeyError
        outcomes[newGame] = n
    end
end

const final_score = 21
const rolls = Dict{Int, Int}(5 => 6, 4 => 3, 6 => 7, 7 => 6, 9 => 1, 8 => 3, 3 => 1)

function part2(p1::Int, p2::Int)
    outcomes = Dict{GameStatus, Int}()
    # outcomes of rolling 3 fair 3-sided dice and adding them up
    initial = GameStatus(Player(p1, 0), Player(p2, 0), false, true)
    outcomes[initial] = 1
    gamesToProcess = [initial, ]
    wins = [0, 0]
    while length(gamesToProcess) > 0
        oldGame = pop!(gamesToProcess)
        player = oldGame.is_player1_turn ? oldGame.player1 : oldGame.player2
        for roll in keys(rolls)
            n::Int = outcomes[oldGame] + rolls[roll]
            new_player::Player = move(player, roll)
            finished = new_player.score >= final_score
            if oldGame.is_player1_turn
                if finished
                    wins[1] += n
                    continue
                else
                    newGame = GameStatus(new_player, oldGame.player2, finished, false)
                end
            else
                # it was player 2's turn
                if finished
                    wins[2] += n
                    continue
                else
                    newGame = GameStatus(oldGame.player1, new_player, finished, true)
                end
            end
            if haskey(outcomes, newGame)
                outcomes[newGame] += n
            else
                push!(gamesToProcess, newGame)
                outcomes[newGame] = n
            end
        end
        println(log10.(wins))
    end
    println(wins)
end
    

part2(4, 8)

