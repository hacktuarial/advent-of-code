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
    


function step(p1::Player, p2::Player, die)
    rolls = rollThreeTimes(die)
    p1 = move(p1, sum(rolls))
    rolls = rollThreeTimes(rolls[end] + 1)
    p2 = move(p2, sum(rolls))
    (p1, p2, rolls[end] + 1)
end


function test()
    setup = (Player(4, 0), Player(8, 0), 1)
    for i in 1:4
        setup = step(setup...)
    end
    setup
end

@assert test()[1] === Player(6, 26)
@assert test()[2] === Player(6, 22)


function part1(p1::Int, p2::Int)
    die = 1
    p1 = Player(p1, 0)
    p2 = Player(p2, 0)
    rolls = 0
    while max(p1.score, p2.score) < 1000
        p1, p2, die = step(p1, p2, die)
        rolls += 6
    end
    println(p1)
    println(p2)
    println(rolls)
    println(rolls * p1.score)
    println(rolls * p2.score)
end


part1(4, 8)




