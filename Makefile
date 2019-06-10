BASH = $(which bash)

install:
	@${BASH} bin/install.sh

authors:
	@${BASH} bin/create_authors.sh

posts:
	@${BASH} bin/create_posts.sh
