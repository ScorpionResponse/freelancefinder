
get_password:
	cat /vagrant/vault-password.file > ~/vault-password.file

requirements:
	ansible-galaxy install -f -r requirements.yml

vault:
	ansible-vault edit --vault-password-file=~/vault-password.file group_vars/all/secrets.yml

dbservers:
	ansible-playbook -i vagrant dbservers.yml --vault-password-file=~/vault-password.file

webservers:
	ansible-playbook -i vagrant webservers.yml --vault-password-file=~/vault-password.file

site: requirements
	ansible-playbook -i vagrant site.yml --vault-password-file=~/vault-password.file

bootstrap: get_password requirements
	ansible-playbook -i vagrant bootstrap.yml -e "ansible_ssh_user=ubuntu" -e "ansible_ssh_pass=vagrant" --vault-password-file=~/vault-password.file

deploy:
	ansible-playbook -i vagrant deploy.yml --vault-password-file=~/vault-password.file
