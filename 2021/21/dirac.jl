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
end


function update(outcomes::Dict{GameStatus, Int}, previousGame::GameStatus, newGame::GameStatus, n::Int)
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
    outcomes
end

function part2(p1::Int, p2::Int)
    final_score = 21
    outcomes = Dict{GameStatus, Int}()
    # outcomes of rolling 3 fair 3-sided dice and adding them up
    rolls = Dict{Int, Int}(5 => 6, 4 => 3, 6 => 7, 7 => 6, 9 => 1, 8 => 3, 3 => 1)
    outcomes[GameStatus(Player(p1, 0), Player(p2, 0))] = 1
    iter = 0
    while true
        iter += 1
        n_before = sum(values(outcomes))
        for oldGame in keys(outcomes)
            for p1_roll in keys(rolls)
                for p2_roll in keys(rolls)
                    if max(oldGame.player1.score, oldGame.player2.score) >= final_score
                        continue
                    end
                    new_p1::Player = move(oldGame.player1, p1_roll)
                    newGame = GameStatus(new_p1, oldGame.player2)
                    outcomes = update(outcomes, oldGame, newGame, rolls[p1_roll])
                    if new_p1.score < final_score
                        # player2 gets a turn
                        new_p2::Player = move(oldGame.player2, p2_roll)
                        newGame = GameStatus(new_p1, new_p2)
                        outcomes = update(outcomes, oldGame, newGame, rolls[p2_roll])
                    end
                end
            end
        end
        n_after = sum(values(outcomes))
        println(n_after)
        if n_before === n_after
            break
        end
    end
    # now, count up how many times each player won
    # finished_games = filter(outcomes, (status, n_times) => (max(status.player1.score, status.player2.score >= final_score))
    # println(outcomes)
    p1 = 0
    p2 = 0
    for (key, value) in outcomes
        if key.player1.score >= final_score
            p1 += value
        elseif key.player2.score >= final_score
            p2 += value
        end
    end
    println(p1)
    println(p2)
end
    

part2(4, 8)

