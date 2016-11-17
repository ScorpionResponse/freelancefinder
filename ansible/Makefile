
get_password:
	cat /vagrant/vault-password.file > ~/vault-password.file

vault:
	ansible-vault edit --vault-password-file=~/vault-password.file vars/secrets.yml

dbservers:
	ansible-playbook -i vagrant dbservers.yml --vault-password-file=~/vault-password.file

webservers:
	ansible-playbook -i vagrant webservers.yml --vault-password-file=~/vault-password.file

site:
	ansible-playbook -i vagrant site.yml --vault-password-file=~/vault-password.file

bootstrap:
	ansible-playbook -i vagrant bootstrap.yml -e "ansible_ssh_user=root" -e "ansible_ssh_pass=vagrant" --vault-password-file=~/vault-password.file
