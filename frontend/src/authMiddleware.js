import jwtDecode from 'jwt-decode'
//import store from './store'
import tokenService from './tokenService'

export default async function (to, from, next){
    const token = localStorage.getItem('accessToken')
    if(token){
        try{
            const payload = jwtDecode(token)
            const tokenExpiration = new Date(payload.exp * 1000)
            
            if (tokenExpiration < new Date()){
                //store.commit('removeToken')
                next('/login')
            }else{
                console.log('aun no se cierra la session')
                const newToken = await tokenService.getNewAccessToken()
                console.log(newToken)
                next()
            }
        }catch(error){
            //store.commit('removeToken')
            next('/login')
        }
    }else{
        //store.commit('removeToken')
        next('/login')
    }

}