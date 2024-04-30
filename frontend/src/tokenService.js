import axios from 'axios';

async function getNewAccessToken() { console.log('nuevo token obtenido desde los componentes')
  try {
    const refreshToken = localStorage.getItem('refreshToken')
    const response = await axios.post(`${process.env.VUE_APP_API_URL}/api/token/refresh/`, {
      refresh: refreshToken,
    });
    const newAccessToken = response.data.access
    localStorage.setItem('accessToken', newAccessToken)
    return newAccessToken
  } catch (error) {
    console.error('Error al obtener el nuevo token de acceso', error);
    throw error; // Propaga el error para manejarlo donde sea necesario
  }
}

export default {
  getNewAccessToken,
  // Otras funciones relacionadas con tokens si las necesitas
};
