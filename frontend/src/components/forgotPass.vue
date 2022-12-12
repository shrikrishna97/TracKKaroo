<template>
    <div class="vue-tempalte">
        <form>
            <h3>Forgot Password</h3>
 
            <div class="form-group">
                <label>Email address</label>
                <input type="email" class="form-control form-control-lg" />
            </div>
 
            <button type="submit" class="btn btn-dark btn-outline-primary btn-lg">Reset password</button>
 
        </form>
    </div>
</template>
 
<script>
    export default {
        name:'forgot',
        data() {
            return {}
        }
    }
</script>