import { io } from 'socket.io-client'
import { socketio_port} from '../../../../sites/common_site_config.json'

export function initSocket() {
  let host = window.location.hostname
  let siteName = window.site_name
  let port = window.location.port ? `:${socketio_port}` : ''
  let protocol = port ? 'http' : 'https'
  let url = `${protocol}://${host}${port}/${siteName}`
  console.log(url)
  let socket = io(url, {
    withCredentials: true,
    reconnectionAttempts: 5,
  })

  // socket.on('global_admin_notifications', (data) => {
  //   console.log('Received applejuice event:', data);
  // });

  return socket
}
