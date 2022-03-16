<script>
    import { createEventDispatcher } from 'svelte'
    import { scale } from 'svelte/transition'

    let dispatch = createEventDispatcher()

    let player1
    let player2
    let sets = 3
    let serve = true
    let isError = false
	$: errors = ['','']

    const inputValidation = (player1, player2) => {
        isError = false
	    errors = ['','']
        let p1_ok = true
        let p2_ok = true
        const chars = 'aąbcćdeęfghijklłmnoópqrsśtuvwxyzźż. '
        // check player 1
        if(player1){
            let p1_lower = player1.toLowerCase()
            for(let i = 0; i < p1_lower.length; i++){
                if(chars.includes(p1_lower[i])){
                    continue
                }else{
                    p1_ok = false
                    errors[0] = 'Remove special characters'
                    break
                }
            }
        }else{
            p1_ok = false
            errors[0] = 'Cannot be empty'
        }

        // check player 2
        if(player2){
            let p2_lower = player2.toLowerCase()
            for(let i = 0; i < p2_lower.length; i++){
                if(chars.indexOf(p2_lower[i]) > -1){
                    continue
                }else{
                    p2_ok = false
                    errors[1] = 'Remove special characters'
                    break
                }
            }
        }else{
            p1_ok = false
            errors[1] = 'Cannot be empty'
        }

        if(p1_ok && p2_ok){
            return true
        }else{
            return false
        }
	}

    const handleStart = () => {
        const data = {
            player1,
            player2,
            sets,
            serve
        }
        // validation
        if(inputValidation(player1, player2)){
            isError = false
            dispatch('setGame', data)
        }else{
            isError = true
        }
    }
    const handleSets = () => {
        if(sets === 3){
            sets = 5
        }else{
            sets = 3
        }
    }
    const handleServe = (e) => {
        serve = !serve
    }
</script>

<form>
    <div class="player">
        <input type="text" placeholder="Player 1 name" bind:value={player1}>
        {#if serve}
            <button on:click|preventDefault={handleServe} id="s1" class={serve ? 'active' : ''} disabled>Serving</button>
        {:else}
            <button on:click|preventDefault={handleServe} id="s1" class={serve ? 'active' : ''}>Serving</button>
        {/if}
        {#if isError}
            <div in:scale class="error">{errors[0]}</div><br>
        {/if}
    </div>
    <div class="player">
        <input type="text" placeholder="Player 2 name" bind:value={player2}>
        {#if serve}
            <button on:click|preventDefault={handleServe} id="s2" class={!serve ? 'active' : ''}>Serving</button>
        {:else}
            <button on:click|preventDefault={handleServe} id="s2" class={!serve ? 'active' : ''} disabled>Serving</button>
        {/if}
        {#if isError}
            <div in:scale class="error">{errors[1]}</div><br>
        {/if}
    </div>
    <div class="num">Number of sets</div>
    {#if sets === 3}
        <button on:click|preventDefault={handleSets} id="set3" class={sets === 3 ? 'active' : ''} disabled>3</button>
    {:else}
        <button on:click|preventDefault={handleSets} id="set3" class={sets === 3 ? 'active' : ''}>3</button>
    {/if}
    {#if sets === 5}
        <button on:click|preventDefault={handleSets} id="set5" class={sets === 5 ? 'active' : ''} disabled>5</button><br>
    {:else}
        <button on:click|preventDefault={handleSets} id="set5" class={sets === 5 ? 'active' : ''}>5</button><br>
    {/if}
    <button on:click|preventDefault={handleStart}>Start new game</button>
</form>

<style>
    .active{
        background-color: var(--blue);
    }
    button:disabled{
        color: white;
        font-weight: 500;
    }
    .num{
        display: inline-block;
        font-weight: 500;
    }
    .error{
        display: inline-block;
        color: red
    }
</style>