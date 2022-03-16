<!-- TODO -->
<!-- undo -->


<script>
	import { fade, scale } from 'svelte/transition'
	import Form from './Form.svelte'
	
	//test
	let test = 'abcdefgh'
	test.indexOf('a')
	let num_of_sets = 3
	let set = 0
	let tiebreak = false
	let tiebreaker = 0
	let tie_first_serving = 1
	let players = [
		{
			id: 1,
			name: 'player 1',
			games: [0, 0, 0, 0, 0],
			sets: 0,
			point_index: 0,
			tie_pts: [0, 0, 0, 0, 0],
			is_tie: [false, false, false, false, false],
			serving: false
		},
		{
			id: 2,
			name: 'player 2',
			games: [0, 0, 0, 0, 0],
			sets: 0,
			point_index: 0,
			tie_pts: [0, 0, 0, 0, 0],
			is_tie: [false, false, false, false, false],
			serving: false
		},
	]
	let clean_players = JSON.parse(JSON.stringify(players))
	let points = ['0', '15', '30', '40', 'Adv']
	let comment = ''
	let matchpoint = false
	let setpoint = false
	let over = true

	let history = []
	let history_ind = 0
	let enable_history = false

	const handlePoints = (player, opponent) => {
		let player1 = null
		let player2 = null

		const whoIsWho = (player, opponent) => {
			if(player.id === 1){
				player1 = player
				player2 = opponent
			}else{
				player1 = opponent
				player2 = player
			}
		}

		const changeServe = () => {
			player.serving = !player.serving
			opponent.serving = !opponent.serving
		}
		const fadeOutComment = (txt, time) => {
			comment = txt
			setTimeout(()=> {
				comment = ''
			}, time);
		}
		// Check for win
		const checkWin = () => {
			if( (num_of_sets === 3 && player.sets === 2) || (num_of_sets === 5 && player.sets === 3) ){
				fadeOutComment(`${player.name} won!`, 5000)
				return true
			}else{
				return false
			}
		}
		// Check for set
		const checkSet = () => {
			if( (player.games[set] === 6 && opponent.games[set] < 5) || player.games[set] === 7){
				player.sets++
				let won = checkWin()
				if(!won){
					set++
				}else{
					over = true
					player.serving = false
					opponent.serving = false
				}
			}
		}
		// Check for matchpoint
		const checkMatchpoint = (player1, player2) => {
			if(!tiebreak){
				if(num_of_sets === 3 &&
					(
					(player1.sets === 1 &&
					( (player1.games[set] > 4 && player2.games[set] < 5) || (player1.games[set] === 6 && player2.games[set] === 5) ) &&
					player1.point_index > 2 && player1.point_index > player2.point_index) ||
					(player2.sets === 1 &&
					( (player2.games[set] > 4 && player1.games[set] < 5) || (player2.games[set] === 6 && player1.games[set] === 5) ) &&
					player2.point_index > 2 && player2.point_index > player1.point_index)
					)){
						matchpoint = true
					}
				if(num_of_sets === 5 &&
					(
					(player1.sets === 2 &&
					( (player1.games[set] > 4 && player2.games[set] < 5) || (player1.games[set] === 6 && player2.games[set] === 5) ) &&
					player1.point_index > 2 && player1.point_index > player2.point_index) ||
					(player2.sets === 2 &&
					( (player2.games[set] > 4 && player1.games[set] < 5) || (player2.games[set] === 6 && player1.games[set] === 5) ) &&
					player2.point_index > 2 && player2.point_index > player1.point_index)
					)){
						matchpoint = true
					}
			}else{
				if(
					(num_of_sets === 3 &&
					(
					(player1.sets === 1 &&
					(player1.tie_pts[set] > 5 && player1.tie_pts[set] > player2.tie_pts[set]) ) ||
					(player2.sets === 1 &&
					(player2.tie_pts[set] > 5 && player2.tie_pts[set] > player1.tie_pts[set]) ) )
					) ||
					(num_of_sets === 5 &&
					(
					(player1.sets === 2 &&
					(player1.tie_pts[set] > 5 && player1.tie_pts[set] > player2.tie_pts[set]) ) ||
					(player2.sets === 1 &&
					(player2.tie_pts[set] > 5 && player2.tie_pts[set] > player1.tie_pts[set]) ) )
					)
				){
					matchpoint = true
				}
			}
			
		}
		// Check for setpoint
		const checkSetpoint = (player1, player2) => {
			if(!tiebreak){
				if(
					(
						(
							(player1.games[set] === 5 && player2.games[set] < 5) ||
							(player1.games[set] === 6 && player2.games[set] === 5)
						) && (player1.point_index > 2 && player1.point_index > player2.point_index)
					) ||
					(
						(
							(player2.games[set] === 5 && player1.games[set] < 5) ||
							(player2.games[set] === 6 && player1.games[set] === 5)
						) && (player2.point_index > 2 && player2.point_index > player1.point_index)
					)
				){
					setpoint = true
				}
			}else{
				if(
					(player1.tie_pts[set] > 5 && player1.tie_pts[set] > player2.tie_pts[set]) ||
					(player2.tie_pts[set] > 5 && player2.tie_pts[set] > player1.tie_pts[set])
				){
					setpoint = true
				}
			}
		}
		// Check for breakpoint
		const checkBreakpoint = () => {
			matchpoint = false
			setpoint = false
			whoIsWho(player, opponent)
			checkSetpoint(player1, player2)
			checkMatchpoint(player1, player2)

			let state = ''
			if(matchpoint){
				state = 'MATCH'
			}else if(setpoint){
				state = 'SET'
			}
			if(!tiebreak){
				if(
					(matchpoint || setpoint) &&
					(
						(player1.point_index > 2 && player1.point_index - player2.point_index === 3) ||
						(player2.point_index > 2 && player2.point_index - player1.point_index === 3)
					) ){
						fadeOutComment(`3 ${state} POINTS`, 2000)
				}else if(
					(player1.point_index > 2 && player1.point_index - player2.point_index === 3 && player2.serving) ||
					(player2.point_index > 2 && player2.point_index - player1.point_index === 3 && player1.serving) ){
						fadeOutComment(`3 BREAK POINTS`, 2000)
				}else if(
					(matchpoint || setpoint) &&
					(
						(player1.point_index > 2 && player1.point_index - player2.point_index === 2) ||
						(player2.point_index > 2 && player2.point_index - player1.point_index === 2)
					) ){
						fadeOutComment(`2 ${state} POINTS`, 2000)
				}else if(
					(player1.point_index > 2 && player1.point_index - player2.point_index === 2 && player2.serving) ||
					(player2.point_index > 2 && player2.point_index - player1.point_index === 2 && player1.serving) ){
						fadeOutComment(`2 BREAK POINTS`, 2000)
				}else if(
					(matchpoint || setpoint) &&
					(
						(player1.point_index > 2 && player1.point_index > player2.point_index) ||
						(player2.point_index > 2 && player2.point_index > player1.point_index)
					) ){
						fadeOutComment(`${state} POINT`, 2000)
				}else if(
					(player1.point_index > 2 && player1.point_index > player2.point_index && player2.serving) ||
					(player2.point_index > 2 && player2.point_index > player1.point_index && player1.serving) ){
						fadeOutComment('BREAK POINT', 2000)
					}
				}else{
					if(
						(player1.tie_pts[set] > 5 && player1.tie_pts[set] > player2.tie_pts[set]) ||
						(player2.tie_pts[set] > 5 && player2.tie_pts[set] > player1.tie_pts[set]) ){
							fadeOutComment(`${state} POINT`, 2000)
					}
			}

		}

		const checkTiebreak = () => {
			whoIsWho(player, opponent)
			if(player.games[set] === 6 && opponent.games[set] === 6){
				tiebreak = true
				if(player1.serving){
					tie_first_serving = 1
				}else{
					tie_first_serving = 2
				}
			}
		}

		const checkServing4Set = () => {
			whoIsWho(player, opponent)
			if(
				(player1.serving && 
				(
					(player1.games[set] > 4 && player2.games[set] < 5) ||
					(player1.games[set] === 6 && player2.games[set] === 5)
				)) ||
				(player2.serving && 
				(
					(player2.games[set] > 4 && player1.games[set] < 5) ||
					(player2.games[set] === 6 && player1.games[set] === 5)
				))
			){
				fadeOutComment('SERVING FOR THE SET', 2000)
			}
		}
		const checkServing4Match = () => {
			whoIsWho(player, opponent)
			if(
				(
					num_of_sets === 3 &&
					(
						(
							(player1.serving && player1.sets === 1) &&
							( (player1.games[set] > 4 && player2.games[set] < 5) || (player1.games[set] === 6 && player2.games[set] === 5) )
						) ||
						(
							(player2.serving && player2.sets === 1) &&
							( (player2.games[set] > 4 && player1.games[set] < 5) || (player2.games[set] === 6 && player1.games[set] === 5) )
						)
					)
				) ||
				(
					num_of_sets === 5 &&
					(
						(
							(player1.serving && player1.sets === 2) &&
							( (player1.games[set] > 4 && player2.games[set] < 5) || (player1.games[set] === 6 && player2.games[set] === 5) )
						) ||
						(
							(player2.serving && player2.sets === 2) &&
							( (player2.games[set] > 4 && player1.games[set] < 5) || (player2.games[set] === 6 && player1.games[set] === 5) )
						)
					)
				)
			){
				fadeOutComment('SERVING FOR THE MATCH', 2000)
				return true
			}else{
				return false
			}
		}

		if(!tiebreak){
			// 40
			if(player.point_index === 3){
				// 40:0, 40:15, 40:30
				if(opponent.point_index < 3){
					player.point_index = 0
					opponent.point_index = 0
					// Check for set
					player.games[set]++
					checkSet()
					if(!over){
						changeServe()
						checkTiebreak()
						let s4m = checkServing4Match()
						if(!s4m){
							checkServing4Set()
						}
					}
				// 40:Adv
				}else if(opponent.point_index === 4){
					opponent.point_index--
				// Deuce
				}else{
					player.point_index++
					checkBreakpoint()
				}
			// Adv
			}else if(player.point_index === 4){
				player.point_index = 0
				opponent.point_index = 0
				player.games[set]++
				// Check for set
				checkSet()
				if(!over){
					changeServe()
					checkTiebreak()
					let s4m = checkServing4Match()
					if(!s4m){
						checkServing4Set()
					}
				}
			}else{
				player.point_index++
				checkBreakpoint()
			}
		// TIEBREAKER
		}else{
			player.tie_pts[set]++
			tiebreaker++
			
			if(player.tie_pts[set] > 6 && (player.tie_pts[set] > opponent.tie_pts[set] + 1) ){
				player.is_tie[set] = true
				opponent.is_tie[set] = true
				player.games[set]++
				checkSet()
				tiebreak = false
				
				whoIsWho(player, opponent)
				if(tie_first_serving === player1.id){
					if(!over){
						changeServe()
					}
				}
			}
			if(tiebreaker === 1 || (tiebreaker > 1 && tiebreaker % 2 !== 0) ){
				if(!over){
					changeServe()
				}
			}
			checkBreakpoint()
		}

		if(player.id === 1){
			players = [player, opponent]
		}else{
			players = [opponent, player]
		}
		// if there was undo then delete unnecessary history
		while(history_ind < history.length - 1){
			history.pop()
		}
		addToHistory(set, tiebreak, tiebreaker, tie_first_serving, players, matchpoint, setpoint, over)
	}
	// left/right arrows for faster point adding
	window.addEventListener('keydown', (e)=>{
		if(!over){
			if(e.code === 'ArrowLeft'){
				handlePoints(players[0], players[1])
			}
			if(e.code === 'ArrowRight'){
				handlePoints(players[1], players[0])
			}
		}
	})
	
	const setGame = (e) => {
		resetData()
		players[0].name = e.detail.player1
		players[1].name = e.detail.player2
		num_of_sets = e.detail.sets
		if(e.detail.serve){
			players[0].serving = true
		}else{
			players[1].serving = true
		}
		over = false
		addToHistory(set, tiebreak, tiebreaker, tie_first_serving, players, matchpoint, setpoint, over)
		history_ind = 0
		enable_history = true

	}
	const resetData = () => {
		num_of_sets = 3
		set = 0
		tiebreak = false
		tiebreaker = 0
		tie_first_serving = 1
		players = JSON.parse(JSON.stringify(clean_players))
		matchpoint = false
		setpoint = false
		over = true
		history = []
	}
	const addToHistory = (set, tiebreak, tiebreaker, tie_first_serving, players, matchpoint, setpoint, over) => {
		const new_score = {
			set,
			tiebreak,
			tiebreaker,
			tie_first_serving,
			players: JSON.parse(JSON.stringify(players)),
			matchpoint,
			setpoint,
			over
		}
		history.push(new_score)
		history_ind++
	}
	const handleHistory = (direction) => {
		if(direction === 'undo'){
			if(history_ind > 0){
				history_ind--
			}
		}else if(direction === 'redo'){
			if(history_ind < history.length - 1)
			history_ind++
		}
		set = history[history_ind].set
		tiebreak = history[history_ind].tiebreak
		tiebreaker = history[history_ind].tiebreaker
		tie_first_serving = history[history_ind].tie_first_serving
		players = JSON.parse(JSON.stringify(history[history_ind].players))
		matchpoint = history[history_ind].matchpoint
		setpoint = history[history_ind].setpoint
		over = history[history_ind].over
	}
</script>

<main>
	<Form on:setGame={setGame} />
	{#if enable_history && history_ind > 0}
		<button on:click|preventDefault={()=>{handleHistory('undo')}} class="history">Undo</button>
	{:else}
		<button on:click|preventDefault={()=>{handleHistory('undo')}} class="history" disabled>Undo</button>
	{/if}
	{#if enable_history && history_ind < history.length - 1}
		<button on:click|preventDefault={()=>{handleHistory('redo')}} class="history">Redo</button>
	{:else}
		<button on:click|preventDefault={()=>{handleHistory('redo')}} class="history" disabled>Redo</button>
	{/if}
	<div class="wrapper">
        <div class="serve">
			{#if !players[0].serving && !players[1].serving}
				<div in:scale class="box">
					<div class="ball"></div>
				</div>
			{:else if players[0].serving}
				<div in:scale class="p1_serving box">
					<div class="ball"></div>
				</div>
			{:else if players[1].serving}
				<div in:scale class="p2_serving box">
					<div class="ball"></div>
				</div>
			{/if}
        </div>
        <div class="players">
            <div class="name box">
                {players[0].name}
            </div>
            <div class="name box">
                {players[1].name}
            </div>
        </div>
        <div class="scores">
            <div class="player_score">
				{#each Array(num_of_sets) as _, i}
					{#if i <= set && players[0].is_tie[i]}
						<div class="set box">{players[0].games[i]}<sup>{players[0].tie_pts[i]}</sup></div>
					{:else if i <= set}
						<div class="set box">{players[0].games[i]}</div>
					{:else}
						<div class="set box disabled">{players[0].games[i]}</div>
					{/if}
				{/each}
				{#if tiebreak}
                	<div class="game box">{players[0].tie_pts[set]}</div>
				{:else}
                	<div class="game box">{points[players[0].point_index]}</div>
				{/if}
            </div>
            <div class="player_score">
                {#each Array(num_of_sets) as _, i}
					{#if i <= set && players[0].is_tie[i]}
						<div class="set box">{players[1].games[i]}<sup>{players[1].tie_pts[i]}</sup></div>
					{:else if i <= set}
						<div class="set box">{players[1].games[i]}</div>
					{:else}
						<div class="set box disabled">{players[1].games[i]}</div>
					{/if}
				{/each}
                {#if tiebreak}
                	<div class="game box">{players[1].tie_pts[set]}</div>
				{:else}
                	<div class="game box">{points[players[1].point_index]}</div>
				{/if}
            </div>
        </div>
        <div class="btns">
            <button on:click={()=>{handlePoints(players[0], players[1])}} disabled={over || null} id='p1_add' class="box">+</button>
            <button on:click={()=>{handlePoints(players[1], players[0])}} disabled={over || null} id='p2_add' class="box">+</button>
        </div>
    </div>
	{#if comment}
    	<div in:scale out:fade class="comment">{comment}</div>
	{/if}
</main>

<style>
	@import url(
    'https://fonts.googleapis.com/css2?family=Montserrat:wght@300;400;500;600;700;800;900&display=swap'
    );

	*{
		font-family: 'Montserrat', sans-serif;
		text-decoration: none;
		font-weight: 900;
	}
	:root{
		--blue: rgb(41, 171, 226);
		--grey: rgb(66, 66, 66);
		--light_grey: rgb(230, 230, 230);
		--yellow: rgb(235, 255, 115);
		--size: 50px;
	}
	.wrapper{
		display: flex;
		color: var(--grey);
	}
	.box{
		height: var(--size);
		display: flex;
		align-items: center;
		justify-content: center;
		transition: transform 1s;
	}
	
	.serve{
		display: flex;
		flex-direction: column;
		justify-content: center;
	}
	.p1_serving{
		transform: translateY(calc( (var(--size)/2) - var(--size) ));
	}
	.p2_serving{
		transform: translateY(calc(var(--size)/2));
	}
	.ball{
		width: 20px;
		height: 20px;
		background-color: var(--yellow);
		border-radius: 100%;
	}

	.player_score{
		display: flex;
		
	}
	.name{
		text-transform: uppercase;
		min-width: var(--size);
		justify-content: left;
		padding-right: 20px;
		padding-left: 10px;
	}
	.scores{
		display: flex;
		flex-direction: column;
	}
	.set{
		width: var(--size);
	}
	sup{
		font-weight: 500;
		transform: translateY(-7px);
	}
	.game{
		color: var(--blue);
		width: calc(var(--size)*1.6);
	}

	.disabled{
		color: var(--light_grey);
	}
	button{
		margin: 0;
		width: var(--size);
	}
	.history{
		text-align: center;
		font-weight: 400;
		width: auto;
	}
	button:disabled{
		opacity: .5;
	}

	.comment{
		margin-top: 10px;
		margin-left: 30px;
		font-weight: 300;
		text-transform: uppercase;
	}


	/* BORDERS */
	.name:nth-child(1),
	.player_score:nth-child(1){
		border-bottom: 1px solid var(--light_grey);
	}
	.set{
		border-left: 1px solid var(--light_grey);
	}
	.game{
		border-left: 4px solid var(--light_grey);
	}
	.btns .box:nth-child(1){
		margin-bottom: 1px;
	}
</style>