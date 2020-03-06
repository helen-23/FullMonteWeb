import paramiko, sys
import sshtunnel
from multiprocessing import Process

def visualizer():

    with sshtunnel.open_tunnel(
        ("142.1.145.194", 9993),
        ssh_username="Capstone",
        ssh_password="pro929",
        remote_bind_address=('localhost', 8080),
        local_bind_address=('', 8080)
        ) as tunnel:

            client = paramiko.SSHClient()
            client.load_system_host_keys()
            client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            client.connect('142.1.145.194', port=9993, username='Capstone', password='pro929')
            ssh_transp = client.get_transport()

            chan = ssh_transp.open_session()
            # chan.settimeout(3 * 60 * 60)
            chan.setblocking(0)
            outdata, errdata = b'',b''

            chan.exec_command(command="Visualizer --paraview /opt/ParaView-5.7.0/ --data /home/Capstone/docker_sims/")

            while True:  # monitoring process
                # Reading from output streams
                while chan.recv_ready():
                    outdata += chan.recv(1000)
                while chan.recv_stderr_ready():
                    errdata += chan.recv_stderr(1000)
                if chan.exit_status_ready():  # If completed
                    break
            retcode = chan.recv_exit_status()
            ssh_transp.close()