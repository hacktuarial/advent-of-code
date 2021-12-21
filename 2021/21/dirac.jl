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




